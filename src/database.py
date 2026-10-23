from __future__ import annotations

import mysql.connector
from mysql.connector import Error

from src.utils import get_mysql_config


class DatabaseConfigurationError(RuntimeError):
    pass


class DatabaseConnectionError(RuntimeError):
    pass


def get_connection():
    config = get_mysql_config()
    password = config['password']
    if password is None or not password.strip():
        raise DatabaseConfigurationError(
            'MYSQL_PASSWORD is missing or empty. Set it in the project-root .env file.'
        )
    try:
        return mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=password,
            database=config['database'],
        )
        except Error as exc:
        error_code = getattr(exc, 'errno', None) or 'unknown'
        raise DatabaseConnectionError(
            f'MySQL connection failed (error {error_code}): {exc}'
        ) from exc



def fetch_student_records() -> list[dict]:
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT s.student_id, s.name, s.age, s.department, s.semester, "
            "s.cgpa, s.attendance, s.previous_marks, s.assignment_score, "
            "s.internal_marks, s.external_marks, s.coding_skill, "
            "s.communication_skill, s.problem_solving_skill, s.projects, "
            "s.certifications, s.learning_hours, s.internship, "
            "s.online_courses, s.hackathon, "
            "p.predicted_percentage, p.performance_category, "
            "p.career_prediction, p.support_risk "
            "FROM students AS s "
            "LEFT JOIN predictions AS p "
            "ON p.id = ("
            "SELECT MAX(p2.id) FROM predictions AS p2 "
            "WHERE p2.student_id = s.student_id"
            ") "
            "ORDER BY s.student_id"
        )

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()



def insert_student_prediction(student_data: dict) -> bool:
    connection = get_connection()
    cursor = None
    try:
        cursor = connection.cursor()

        query = (
            "INSERT INTO students (student_id, name, age, department, semester, "
            "cgpa, attendance, previous_marks, assignment_score, internal_marks, "
            "external_marks, coding_skill, communication_skill, "
            "problem_solving_skill, projects, certifications, learning_hours, "
            "internship, online_courses, hackathon, created_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s, %s, %s, NOW())"
        )
        values = (
            student_data.get('student_id'),
            student_data.get('name'),
            student_data.get('age'),
            student_data.get('department'),
            student_data.get('semester'),
            student_data.get('cgpa'),
            student_data.get('attendance'),
            student_data.get('previous_marks'),
            student_data.get('assignment_score'),
            student_data.get('internal_marks'),
            student_data.get('external_marks'),
            student_data.get('coding_skill'),
            student_data.get('communication_skill'),
            student_data.get('problem_solving_skill'),
            student_data.get('projects'),
            student_data.get('certifications'),
            student_data.get('learning_hours'),
            student_data.get('internship'),
            student_data.get('online_courses'),
            student_data.get('hackathon'),
        )

        cursor.execute(query, values)
        connection.commit()
        return True
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()
