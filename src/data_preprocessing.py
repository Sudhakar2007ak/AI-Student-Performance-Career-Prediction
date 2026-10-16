from __future__ import annotations

from typing import Any, Dict

import pandas as pd


VALID_CAREER_DOMAINS = [
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

VALID_RISK_LEVELS = ['Low Risk', 'Medium Risk', 'High Risk']

SUPPORT_RISK_FEATURES = [
    'attendance', 'previous_marks', 'assignment_score', 'internal_marks',
    'cgpa', 'learning_hours', 'online_courses', 'projects',
]

NUMERIC_COLUMNS = [
    'attendance', 'previous_marks', 'assignment_score', 'internal_marks', 'external_marks',
    'cgpa', 'coding_skill', 'communication_skill', 'problem_solving_skill', 'projects',
    'certifications', 'learning_hours', 'internship', 'online_courses', 'hackathon',
    'final_percentage', 'age', 'semester'
]


def validate_student_record(record: Dict[str, Any]) -> bool:
    required = [
        'attendance', 'previous_marks', 'assignment_score', 'internal_marks', 'external_marks',
        'cgpa', 'coding_skill', 'communication_skill', 'problem_solving_skill', 'projects',
        'certifications', 'learning_hours', 'internship', 'online_courses', 'hackathon'
    ]
    for key in required:
        if key not in record:
            return False
        value = record[key]
        if value is None or pd.isna(value):
            return False
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            return False
        if numeric_value < 0:
            return False
    attendance = float(record.get('attendance', 0))
    if not 0 <= attendance <= 100:
        return False
    previous_marks = float(record.get('previous_marks', 0))
    if not 0 <= previous_marks <= 100:
        return False
    cgpa = float(record.get('cgpa', 0))
    if not 0 <= cgpa <= 10:
        return False
    return True


def generate_support_risk_labels(df: pd.DataFrame) -> pd.Series:
    missing = [column for column in SUPPORT_RISK_FEATURES if column not in df.columns]
    if missing:
        raise ValueError(f'Missing academic factors for support-risk labels: {", ".join(missing)}')

    factors = df[SUPPORT_RISK_FEATURES].apply(pd.to_numeric, errors='coerce')
    if factors.isna().any().any():
        raise ValueError('Academic factors for support-risk labels must be present and numeric.')

    risk_score = (
        (100 - factors['attendance'].clip(0, 100)) * 0.25
        + (100 - factors['previous_marks'].clip(0, 100)) * 0.20
        + (100 - factors['assignment_score'].clip(0, 100)) * 0.15
        + (100 - factors['internal_marks'].clip(0, 100)) * 0.15
        + (10 - factors['cgpa'].clip(0, 10)) * 10 * 0.15
        + (10 - factors['learning_hours'].clip(0, 10)) * 10 * 0.05
        + (3 - factors['online_courses'].clip(0, 3)) * (100 / 3) * 0.025
        + (2 - factors['projects'].clip(0, 2)) * 50 * 0.025
    )

    labels = pd.Series('High Risk', index=df.index, name='support_risk', dtype='object')
    labels.loc[risk_score < 30] = 'Medium Risk'
    labels.loc[risk_score < 20] = 'Low Risk'
    return labels


def clean_student_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [str(col).strip().lower() for col in cleaned.columns]

    for col in cleaned.columns:
        if col in NUMERIC_COLUMNS:
            cleaned[col] = pd.to_numeric(cleaned[col], errors='coerce')

    cleaned = cleaned.dropna(subset=[
        'attendance', 'previous_marks', 'assignment_score', 'internal_marks', 'external_marks',
        'cgpa', 'coding_skill', 'communication_skill', 'problem_solving_skill', 'projects',
        'certifications', 'learning_hours', 'internship', 'online_courses', 'hackathon'
    ])

    for col in ['attendance', 'previous_marks', 'assignment_score', 'internal_marks', 'external_marks', 'cgpa']:
        cleaned = cleaned[(cleaned[col] >= 0) & (cleaned[col].notna())]

    cleaned['attendance'] = cleaned['attendance'].clip(0, 100)
    cleaned['previous_marks'] = cleaned['previous_marks'].clip(0, 100)
    cleaned['assignment_score'] = cleaned['assignment_score'].clip(0, 100)
    cleaned['internal_marks'] = cleaned['internal_marks'].clip(0, 100)
    cleaned['external_marks'] = cleaned['external_marks'].clip(0, 100)
    cleaned['cgpa'] = cleaned['cgpa'].clip(0, 10)

    if 'final_percentage' in cleaned.columns:
        cleaned['final_percentage'] = cleaned['final_percentage'].clip(0, 100)

    if 'career_domain' in cleaned.columns:
        cleaned['career_domain'] = cleaned['career_domain'].fillna('Data Analyst')
        cleaned['career_domain'] = cleaned['career_domain'].where(cleaned['career_domain'].isin(VALID_CAREER_DOMAINS), 'Data Analyst')

    if 'support_risk' in cleaned.columns:
        cleaned['support_risk'] = cleaned['support_risk'].fillna('Medium Risk')
        cleaned['support_risk'] = cleaned['support_risk'].where(cleaned['support_risk'].isin(VALID_RISK_LEVELS), 'Medium Risk')

    return cleaned.reset_index(drop=True)
