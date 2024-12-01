
--Grades
CREATE OR REPLACE FUNCTION calculate_final_grade()
RETURNS TRIGGER AS $$
BEGIN
    -- Ensure grading percentages are available for the course
    IF NOT EXISTS (SELECT 1 FROM CourseGrading WHERE course_id = NEW.course_id) THEN
        RAISE EXCEPTION 'No grading configuration found for course_id: %', NEW.course_id;
    END IF;

    -- Calculate the final grade based on the weighted components
    UPDATE StudentCourseGrades
    SET grade = (
        COALESCE(NEW.td_grade, 0) * (SELECT COALESCE(td_percentage, 0) FROM CourseGrading WHERE course_id = NEW.course_id) / 100 +
        COALESCE(NEW.tp_grade, 0) * (SELECT COALESCE(tp_percentage, 0) FROM CourseGrading WHERE course_id = NEW.course_id) / 100 +
        COALESCE(NEW.cm_grade, 0) * (SELECT COALESCE(cm_percentage, 0) FROM CourseGrading WHERE course_id = NEW.course_id) / 100 +
        COALESCE(NEW.midterm_grade, 0) * (SELECT COALESCE(midterm_percentage, 0) FROM CourseGrading WHERE course_id = NEW.course_id) / 100 +
        COALESCE(NEW.final_grade, 0) * (SELECT COALESCE(final_percentage, 0) FROM CourseGrading WHERE course_id = NEW.course_id) / 100
    )
    WHERE student_id = NEW.student_id AND course_id = NEW.course_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_final_grade
AFTER INSERT OR UPDATE ON StudentCourseGrades
FOR EACH ROW
EXECUTE FUNCTION calculate_final_grade();


--Fee
CREATE OR REPLACE FUNCTION CalculateFee()
RETURNS TRIGGER AS $$
DECLARE
    total_fee DECIMAL(10, 2) := 0;
    total_credits INT := 0;
    retake_fee DECIMAL(10, 2) := 0;
    discount DECIMAL(10, 2) := 0;
    scholarship DECIMAL(10, 2) := 0;
    credit_fee DECIMAL(10, 2) := 0;
    semester_fee DECIMAL(10, 2) := 0;
BEGIN
    -- Fetch the semester fee for the student's program
    SELECT f.semester_fee
    INTO semester_fee
    FROM Fee f
    JOIN Students s ON s.program_id = f.program_id
    WHERE s.student_id = NEW.student_id
    LIMIT 1;

    -- If no fee is found for the student's program, raise an error
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No fee found for the student program with student_id: %', NEW.student_id;
    END IF;

    -- Calculate credit fee dynamically (assuming 2 semesters per year and 60 credits)
    credit_fee := (semester_fee * 2) / 60;

    -- Calculate total credits for the student's enrolled courses
    SELECT COALESCE(SUM(c.credit), 0)
    INTO total_credits
    FROM Courses c
    JOIN ProgramCourses pc ON c.course_id = pc.course_id
    JOIN Students s ON s.program_id = pc.program_id
    WHERE s.student_id = NEW.student_id;

    -- If no courses are found for the student, raise an error
    IF total_credits = 0 THEN
        RAISE EXCEPTION 'No courses found for student_id: %', NEW.student_id;
    END IF;

    -- Calculate the base fee for the student
    total_fee := total_credits * credit_fee;

    -- Calculate retake fees (if any)
    SELECT COALESCE(SUM(c.credit * credit_fee), 0)
    INTO retake_fee
    FROM FailedCourses f
    JOIN Courses c ON f.course_id = c.course_id
    WHERE f.student_id = NEW.student_id;

    -- Fetch scholarship and discount from Payments table
    SELECT COALESCE(SUM(p.scholarship_discount), 0), COALESCE(SUM(p.academic_discount), 0)
    INTO scholarship, discount
    FROM Payments p
    WHERE p.student_id = NEW.student_id;

    -- Calculate final fee (base fee + retake fee - scholarship - discount)
    total_fee := total_fee + retake_fee - scholarship - discount;

    -- Update the total fee due for the student
    UPDATE Students
    SET total_fee_due = total_fee
    WHERE student_id = NEW.student_id;

    RETURN NULL; -- We don’t need to return anything from this trigger function
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER fee_calculation_trigger
AFTER INSERT OR UPDATE ON Payments
FOR EACH ROW
EXECUTE FUNCTION CalculateFee();



--Course failure
CREATE OR REPLACE FUNCTION calculate_block_pass_or_fail(student_id INT)
RETURNS VOID AS $$
DECLARE
    course_grade DECIMAL(5, 2);
    block_id INT;
    average_grade DECIMAL(5, 2);
    total_grade DECIMAL(10, 2) := 0;
    total_courses INT := 0;
BEGIN
    -- Loop through each block the student is enrolled in
    FOR block_id IN
        SELECT DISTINCT block_id
        FROM ProgramCourses
        JOIN Courses ON ProgramCourses.course_id = Courses.course_id
        WHERE ProgramCourses.program_id = (SELECT program_id FROM Students WHERE student_id = student_id)
    LOOP
        -- Calculate the total grade for all courses in this block
        FOR course_grade IN
            SELECT grade
            FROM StudentCourseGrades
            WHERE student_id = student_id
              AND course_id IN (SELECT course_id FROM ProgramCourses WHERE block_id = block_id)
        LOOP
            total_grade := total_grade + course_grade;
            total_courses := total_courses + 1;
        END LOOP;

        -- Calculate the average grade for the block
        IF total_courses > 0 THEN
            average_grade := total_grade / total_courses;
        ELSE
            average_grade := 0;
        END IF;

        -- Check if the average grade is below 10
        IF average_grade < 10 THEN
            -- Mark courses in the block as failed
            INSERT INTO FailedCourses (student_id, course_id)
            SELECT student_id, course_id
            FROM ProgramCourses
            WHERE block_id = block_id;
        END IF;

        -- Reset counters for the next block
        total_grade := 0;
        total_courses := 0;
    END LOOP;

    RETURN;
END;
$$ LANGUAGE plpgsql;


