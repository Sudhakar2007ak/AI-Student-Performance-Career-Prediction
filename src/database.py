
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
    password = config.get("password")

    if password is None or not str(password).strip():
        raise DatabaseConfigurationError(
            "MYSQL_PASSWORD is missing or empty. "
            "Check the Streamlit Cloud Secrets configuration "
            "or your local .env file."
        )

    try:
        return mysql.connector.connect(
            host=config["host"],
            port=int(config["port"]),
            user=config["user"],
            password=password,
            database=config["database"],
            connection_timeout=15,
            ssl_disabled=False,
        )
    except Error as exc:
        error_code = getattr(exc, "errno", None) or "unknown"
        raise DatabaseConnectionError(
            f"MySQL connection failed (error {error_code}): {exc}"
        ) from exc


def fetch_student_records():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                s.*,
                p.predicted_percentage,
                p.career_prediction,
                p.support_risk
            FROM students AS s
            LEFT JOIN predictions AS p
                ON s.student_id = p.student_id
        """

        cursor.execute(query)
        return cursor.fetchall()

    except Error as exc:
        error_code = getattr(exc, "errno", None) or "unknown"
        raise DatabaseConnectionError(
            f"MySQL query failed (error {error_code}): {exc}"
        ) from exc

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()
