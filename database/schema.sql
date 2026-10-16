CREATE DATABASE IF NOT EXISTS student_career_prediction;
USE student_career_prediction;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    age INT,
    department VARCHAR(100),
    semester INT,
    cgpa DECIMAL(4,2),
    attendance DECIMAL(5,2),
    assignment_score DECIMAL(5,2),
    internal_marks DECIMAL(5,2),
    external_marks DECIMAL(5,2),
    coding_skill INT,
    communication_skill INT,
    problem_solving_skill INT,
    projects INT,
    certifications INT,
    learning_hours DECIMAL(5,2),
    internship INT,
    online_courses INT,
    hackathon INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(100) NOT NULL,
    predicted_percentage DECIMAL(5,2),
    performance_category VARCHAR(50),
    career_prediction VARCHAR(100),
    support_risk VARCHAR(50),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(100) NOT NULL,
    skill_name VARCHAR(255),
    skill_level INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
