CREATE OR REPLACE FUNCTION CalculateFee(student_id INT)
RETURNS VOID AS $$
DECLARE
    total_fee DECIMAL(10, 2);
    total_credits INT;
    retake_fee DECIMAL(10, 2);
    discount DECIMAL(10, 2);
    scholarship DECIMAL(10, 2);
    credit_fee DECIMAL(10, 2);
    semester_fee DECIMAL(10, 2);
BEGIN
    -- Fetch the semester fee for the student's program
    SELECT f.semester_fee
    INTO semester_fee
    FROM Students s
    JOIN Fee f ON s.program_id = f.program_id
    WHERE s.student_id = student_id;

    -- Calculate credit fee dynamically
    credit_fee := (semester_fee * 2) / 60; -- 2 semesters per year, 60 credits total

    -- Calculate total credits for the student's enrolled courses
    SELECT COALESCE(SUM(c.credit), 0)
    INTO total_credits
    FROM Courses c
    JOIN ProgramCourses pc ON c.course_id = pc.course_id
    JOIN Students s ON s.program_id = pc.program_id
    WHERE s.student_id = student_id;

    -- Calculate the base fee
    total_fee := total_credits * credit_fee;

    -- Calculate retake fees (if any)
    SELECT COALESCE(SUM(c.credit * credit_fee), 0)
    INTO retake_fee
    FROM FailedCourses f
    JOIN Courses c ON f.course_id = c.course_id
    WHERE f.student_id = student_id;

    -- Fetch scholarship and discount
    SELECT COALESCE(SUM(p.scholarship_discount), 0), COALESCE(SUM(p.academic_discount), 0)
    INTO scholarship, discount
    FROM Payments p
    WHERE p.student_id = student_id;

    -- Calculate final fee
    total_fee := total_fee + retake_fee - scholarship - discount;

    -- Update the student's fee in the database
    UPDATE Students
    SET total_fee_due = total_fee
    WHERE student_id = student_id;
END;
$$ LANGUAGE plpgsql;
