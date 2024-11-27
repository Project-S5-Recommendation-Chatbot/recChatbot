-- Table for Students
CREATE TABLE Students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(100),
    phone_number VARCHAR(20),
    program_id INT,
    status JSONB, -- Supports multiple statuses like {"year1": true, "year2": true}
    enrollment_date DATE,
    fce_passed BOOLEAN DEFAULT FALSE,
    delf_passed BOOLEAN DEFAULT FALSE,
    total_fee_due DECIMAL(10, 2) DEFAULT 0.00, -- Automatically calculated
    FOREIGN KEY (program_id) REFERENCES Programs(program_id)
);

-- Table for Programs
CREATE TABLE Programs (
    program_id SERIAL PRIMARY KEY,
    program_name VARCHAR(100) NOT NULL,
    duration INT, -- duration in years
    description TEXT
);

-- Table for Courses
CREATE TABLE Courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credit INT NOT NULL,
    hours_cm INT, -- hours for lectures
    hours_td INT, -- hours for tutorials
    hours_tp INT, -- hours for practicals
    hours_std INT, -- hours for self-directed study
    hours_stp INT, -- hours for supervised team projects
    description TEXT
);

-- Junction table for Program-Course relationship
CREATE TABLE ProgramCourses (
    ProgramCourses_id SERIAL PRIMARY KEY,
    program_id INT,
    course_id INT,
    year_number INT,
    semester_number INT,
    FOREIGN KEY (program_id) REFERENCES Programs(program_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Table for Fee
CREATE TABLE Fee (
    fee_id SERIAL PRIMARY KEY,
    program_id INT,
    academic_year INT,
    semester_fee DECIMAL(10, 2),
    monthly_fee DECIMAL(10, 2),
    months_in_semester INT,
    credit_fee DECIMAL(10, 2), -- Per-credit fee
    max_credits_per_year INT DEFAULT 60, -- Maximum credits per year
    FOREIGN KEY (program_id) REFERENCES Programs(program_id)
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
    scholarship_discount DECIMAL(10, 2), -- Added for scholarships
    academic_discount DECIMAL(10, 2), -- Added for academic discounts
    calculated_fee DECIMAL(10, 2) DEFAULT 0.00, -- Automatically calculated
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (fee_id) REFERENCES Fee(fee_id)
);

-- Table for Internships (Stage)
CREATE TABLE Internships (
    internship_id SERIAL PRIMARY KEY,
    student_id INT,
    location VARCHAR(100), -- e.g., Armenia or other country
    duration INT, -- Duration in months
    report_submitted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Table for Course Grading Percentages
CREATE TABLE CourseGrading (
    course_grading_id SERIAL PRIMARY KEY,
    course_id INT,
    td_percentage DECIMAL(5, 2), -- Tutorials percentage in final grade
    tp_percentage DECIMAL(5, 2), -- Practicals percentage in final grade
    cm_percentage DECIMAL(5, 2), -- Lectures percentage in final grade
    midterm_percentage DECIMAL(5, 2), -- Midterm percentage in final grade
    final_percentage DECIMAL(5, 2), -- Final exam percentage in final grade
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Table for Projects per Semester
CREATE TABLE SemesterProjects (
    project_id SERIAL PRIMARY KEY,
    student_id INT,
    program_id INT,
    semester_number INT,
    project_description TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (program_id) REFERENCES Programs(program_id)
);

-- Additional Table for Failed Courses
CREATE TABLE FailedCourses (
    failed_course_id SERIAL PRIMARY KEY,
    student_id INT,
    course_id INT,
    semester_number INT,
    year_number INT,
    credit_fee DECIMAL(10, 2), -- Per-credit fee for retaking
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);




