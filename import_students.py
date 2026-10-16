
import csv
from pathlib import Path

from src.database import get_connection

CSV_FILE = Path("data/student_data.csv")


def number(value, convert=float):
    if value is None or value.strip() == "":
        return None
    return convert(value)


connection = get_connection()
cursor = connection.cursor()

try:
    with CSV_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        count = 0

        for row in reader:
            student_id = row["student_id"]

            # The CSV has no name column, so use student_id as a placeholder.
            cursor.execute(
                """
                INSERT INTO students (
                    student_id, name, attendance, previous_marks, assignment_score,
                    internal_marks, external_marks, cgpa, coding_skill,
                    communication_skill, problem_solving_skill, projects,
                    certifications, learning_hours, internship,
                    online_courses, hackathon
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    attendance = VALUES(attendance),
                    assignment_score = VALUES(assignment_score),
                    internal_marks = VALUES(internal_marks),
                    external_marks = VALUES(external_marks),
                    cgpa = VALUES(cgpa),
                    coding_skill = VALUES(coding_skill),
                    communication_skill = VALUES(communication_skill),
                    problem_solving_skill = VALUES(problem_solving_skill),
                    projects = VALUES(projects),
                    certifications = VALUES(certifications),
                    learning_hours = VALUES(learning_hours),
                    internship = VALUES(internship),
                    online_courses = VALUES(online_courses),
                    hackathon = VALUES(hackathon)
                """,
                (
                    student_id,
                    student_id,
                    number(row["attendance"]),
                    number(row["previous_marks"]), 
                    number(row["assignment_score"]),
                    number(row["internal_marks"]),
                    number(row["external_marks"]),
                    number(row["cgpa"]),
                    number(row["coding_skill"], int),
                    number(row["communication_skill"], int),
                    number(row["problem_solving_skill"], int),
                    number(row["projects"], int),
                    number(row["certifications"], int),
                    number(row["learning_hours"]),
                    number(row["internship"], int),
                    number(row["online_courses"], int),
                    number(row["hackathon"], int),
                ),
            )

            # Update the latest prediction if one exists; otherwise insert it.
            cursor.execute(
                "SELECT id FROM predictions WHERE student_id = %s "
                "ORDER BY id DESC LIMIT 1",
                (student_id,),
            )
            existing = cursor.fetchone()

            prediction_values = (
                number(row["final_percentage"]),
                "Not classified",
                row["career_domain"],
                row["support_risk"],
            )

            if existing:
                cursor.execute(
                    """
                    UPDATE predictions
                    SET predicted_percentage = %s,
                        performance_category = %s,
                        career_prediction = %s,
                        support_risk = %s
                    WHERE id = %s
                    """,
                    (*prediction_values, existing[0]),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO predictions (
                        student_id, predicted_percentage,
                        performance_category, career_prediction, support_risk
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (student_id, *prediction_values),
                )

            count += 1

    connection.commit()
    print(f"Successfully imported or updated {count} student records.")

except Exception:
    connection.rollback()
    raise

finally:
    cursor.close()
    connection.close()
