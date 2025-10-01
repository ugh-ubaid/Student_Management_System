CREATE DATABASE student_management;
USE student_management;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    roll_no VARCHAR(50) UNIQUE NOT NULL,
    course VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);
