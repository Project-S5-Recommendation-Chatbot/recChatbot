-- Table for Students
CREATE TABLE Students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(100),
    phone_number VARCHAR(20),
    program_id INT,
    status VARCHAR(50), -- Supports statuses for multiple years
    enrollment_date DATE,
    total_fee_due DECIMAL(10, 2),
    FOREIGN KEY (program_id) REFERENCES Programs(program_id)
);

-- Table for Programs
CREATE TABLE Programs (
    program_id SERIAL PRIMARY KEY,
    program_name VARCHAR(100) NOT NULL,
    duration INT, -- Duration in years
    description TEXT
);

-- Table for Fee
CREATE TABLE Fee (
    fee_id SERIAL PRIMARY KEY,
    program_id INT,
    academic_year INT,
    semester_fee DECIMAL(10, 2), -- Fee per semester
    monthly_fee DECIMAL(10, 2), -- Monthly fee
    months_in_semester INT, -- Months in each semester
    max_credits_per_year INT DEFAULT 60, -- Maximum credits in a year
    FOREIGN KEY (program_id) REFERENCES Programs(program_id)
);

-- Table for Courses
CREATE TABLE Courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credit INT, -- Number of credits
    hours_cm INT, -- Lecture hours
    hours_td INT, -- Tutorial hours
    hours_tp INT, -- Practical hours
    std_percentage DECIMAL(5, 2), -- Percentage of TD in grade
    stp_percentage DECIMAL(5, 2), -- Percentage of TP in grade
    description TEXT
);

-- Junction Table for Program-Course Relationship
CREATE TABLE ProgramCourses (
    program_course_id SERIAL PRIMARY KEY,
    program_id INT,
    course_id INT,
    year_number INT,
    semester_number INT,
    FOREIGN KEY (program_id) REFERENCES Programs(program_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Table for Payments
CREATE TABLE Payments (
    payment_id SERIAL PRIMARY KEY,
    student_id INT,
    fee_id INT,
    payment_amount DECIMAL(10, 2),
    payment_type VARCHAR(50),
    payment_date DATE,
    due_date DATE,
    status VARCHAR(20),
    scholarship_discount DECIMAL(10, 2) DEFAULT 0.00,
    academic_discount DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (fee_id) REFERENCES Fee(fee_id)
);

-- Table for Failed Courses
CREATE TABLE FailedCourses (
    failed_course_id SERIAL PRIMARY KEY,
    student_id INT,
    course_id INT,
    semester_number INT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Table for Internships (Stages)
CREATE TABLE Internships (
    internship_id SERIAL PRIMARY KEY,
    student_id INT,
    location VARCHAR(100), -- Location of internship
    country VARCHAR(100), -- Country of internship
    duration_in_months INT, -- Duration in months
    report_submitted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

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
