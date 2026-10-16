from __future__ import annotations

import random
from pathlib import Path
import sys

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_preprocessing import generate_support_risk_labels


CAREERS = [
    'Data Scientist',
    'AI/ML Engineer',
    'Data Analyst',
    'Web Developer',
    'Software Developer',
    'Cybersecurity Analyst',
    'Cloud Engineer',
    'DevOps Engineer',
    'Database Administrator',
    'UI/UX Designer',
]


def generate_demo_dataset(rows: int = 500) -> pd.DataFrame:
    records = []
    rng = random.Random(42)
    career_profiles = {
        'Data Scientist': {'coding_skill': (6, 10), 'communication_skill': (5, 8), 'problem_solving_skill': (7, 10), 'projects': (2, 6), 'certifications': (2, 7), 'learning_hours': (10, 20), 'online_courses': (4, 8), 'hackathon': (1, 3)},
        'AI/ML Engineer': {'coding_skill': (7, 10), 'communication_skill': (5, 8), 'problem_solving_skill': (8, 10), 'projects': (3, 7), 'certifications': (3, 8), 'learning_hours': (12, 22), 'online_courses': (5, 9), 'hackathon': (1, 3)},
        'Data Analyst': {'coding_skill': (5, 8), 'communication_skill': (6, 9), 'problem_solving_skill': (6, 8), 'projects': (1, 5), 'certifications': (2, 6), 'learning_hours': (8, 18), 'online_courses': (3, 7), 'hackathon': (0, 2)},
        'Web Developer': {'coding_skill': (6, 9), 'communication_skill': (5, 8), 'problem_solving_skill': (6, 8), 'projects': (2, 6), 'certifications': (1, 5), 'learning_hours': (9, 18), 'online_courses': (4, 8), 'hackathon': (1, 3)},
        'Software Developer': {'coding_skill': (6, 9), 'communication_skill': (5, 8), 'problem_solving_skill': (7, 9), 'projects': (2, 6), 'certifications': (2, 6), 'learning_hours': (10, 18), 'online_courses': (3, 7), 'hackathon': (1, 3)},
        'Cybersecurity Analyst': {'coding_skill': (5, 8), 'communication_skill': (5, 8), 'problem_solving_skill': (7, 9), 'projects': (1, 5), 'certifications': (2, 6), 'learning_hours': (8, 16), 'online_courses': (3, 7), 'hackathon': (0, 2)},
        'Cloud Engineer': {'coding_skill': (6, 9), 'communication_skill': (5, 8), 'problem_solving_skill': (6, 9), 'projects': (2, 6), 'certifications': (2, 6), 'learning_hours': (10, 18), 'online_courses': (4, 8), 'hackathon': (1, 3)},
        'DevOps Engineer': {'coding_skill': (6, 9), 'communication_skill': (4, 7), 'problem_solving_skill': (6, 9), 'projects': (2, 6), 'certifications': (2, 6), 'learning_hours': (9, 18), 'online_courses': (4, 8), 'hackathon': (1, 3)},
        'Database Administrator': {'coding_skill': (5, 8), 'communication_skill': (5, 8), 'problem_solving_skill': (6, 8), 'projects': (1, 5), 'certifications': (2, 6), 'learning_hours': (7, 16), 'online_courses': (2, 6), 'hackathon': (0, 2)},
        'UI/UX Designer': {'coding_skill': (4, 7), 'communication_skill': (7, 10), 'problem_solving_skill': (5, 8), 'projects': (2, 6), 'certifications': (1, 5), 'learning_hours': (7, 15), 'online_courses': (2, 6), 'hackathon': (0, 2)},
    }

    for _ in range(rows):
        career = rng.choice(CAREERS)
        profile = career_profiles[career]

        attendance = rng.randint(52, 99)
        previous_marks = rng.randint(50, 97)
        assignment_score = rng.randint(55, 99)
        internal_marks = rng.randint(50, 96)
        external_marks = rng.randint(45, 95)
        cgpa = round(rng.uniform(5.0, 9.8), 2)
        coding_skill = rng.randint(*profile['coding_skill'])
        communication_skill = rng.randint(*profile['communication_skill'])
        problem_solving_skill = rng.randint(*profile['problem_solving_skill'])
        projects = rng.randint(*profile['projects'])
        certifications = rng.randint(*profile['certifications'])
        learning_hours = rng.randint(*profile['learning_hours'])
        internship = rng.randint(0, 2)
        online_courses = rng.randint(*profile['online_courses'])
        hackathon = rng.randint(*profile['hackathon'])

        academic_base = (
            attendance * 0.32 + previous_marks * 0.24 + assignment_score * 0.18 + internal_marks * 0.14 + external_marks * 0.12
        )
        skill_bonus = (
            coding_skill * 2.0 + communication_skill * 1.3 + problem_solving_skill * 2.3 + projects * 3.2 + certifications * 2.5 + learning_hours * 0.8
        )
        final_percentage = min(100, max(38, round((academic_base + skill_bonus) / 4.5, 2)))

        records.append({
            'attendance': attendance,
            'previous_marks': previous_marks,
            'assignment_score': assignment_score,
            'internal_marks': internal_marks,
            'external_marks': external_marks,
            'cgpa': cgpa,
            'coding_skill': coding_skill,
            'communication_skill': communication_skill,
            'problem_solving_skill': problem_solving_skill,
            'projects': projects,
            'certifications': certifications,
            'learning_hours': learning_hours,
            'internship': internship,
            'online_courses': online_courses,
            'hackathon': hackathon,
            'career_domain': career,
            'final_percentage': final_percentage,
        })

    df = pd.DataFrame(records)
    df.insert(0, 'student_id', [f'STU-{i:04d}' for i in range(1, rows + 1)])
    df['support_risk'] = generate_support_risk_labels(df)
    return df


if __name__ == '__main__':
    output_path = ROOT_DIR / 'data' / 'student_data.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = generate_demo_dataset(500)
    df.to_csv(output_path, index=False)
    print(f'Generated {len(df)} synthetic records at {output_path}')
    for risk, count in df['support_risk'].value_counts().reindex(
        ['Low Risk', 'Medium Risk', 'High Risk'], fill_value=0
    ).items():
        print(f'{risk}: {count}')
