import pandas as pd

from src.data_preprocessing import clean_student_data, generate_support_risk_labels, validate_student_record


def test_validate_student_record_accepts_valid_input():
    data = {
        'attendance': 88,
        'previous_marks': 82,
        'assignment_score': 90,
        'internal_marks': 80,
        'external_marks': 78,
        'cgpa': 8.6,
        'coding_skill': 7,
        'communication_skill': 6,
        'problem_solving_skill': 8,
        'projects': 2,
        'certifications': 3,
        'learning_hours': 10,
        'internship': 1,
        'online_courses': 4,
        'hackathon': 1,
    }
    assert validate_student_record(data) is True


def test_clean_student_data_removes_invalid_rows():
    df = pd.DataFrame([
        {'attendance': 98, 'previous_marks': 90, 'assignment_score': 82, 'internal_marks': 84, 'external_marks': 80,
         'cgpa': 8.7, 'coding_skill': 8, 'communication_skill': 7, 'problem_solving_skill': 8,
         'projects': 2, 'certifications': 3, 'learning_hours': 9, 'internship': 1, 'online_courses': 3,
         'hackathon': 1, 'career_domain': 'Data Scientist', 'final_percentage': 82.1, 'support_risk': 'Low Risk'},
        {'attendance': -5, 'previous_marks': 50, 'assignment_score': 90, 'internal_marks': 88, 'external_marks': 79,
         'cgpa': 7.5, 'coding_skill': 6, 'communication_skill': 5, 'problem_solving_skill': 7,
         'projects': 1, 'certifications': 1, 'learning_hours': 6, 'internship': 0, 'online_courses': 2,
         'hackathon': 0, 'career_domain': 'AI/ML Engineer', 'final_percentage': 75.0, 'support_risk': 'Medium Risk'}
    ])
    cleaned = clean_student_data(df)
    assert len(cleaned) == 1
    assert 'final_percentage' in cleaned.columns


def test_generate_support_risk_labels_uses_all_three_levels():
    factors = pd.DataFrame([
        {'attendance': 100, 'previous_marks': 100, 'assignment_score': 100, 'internal_marks': 100,
         'cgpa': 10, 'learning_hours': 15, 'online_courses': 5, 'projects': 4},
        {'attendance': 80, 'previous_marks': 80, 'assignment_score': 80, 'internal_marks': 80,
         'cgpa': 8, 'learning_hours': 8, 'online_courses': 2, 'projects': 1},
        {'attendance': 50, 'previous_marks': 50, 'assignment_score': 50, 'internal_marks': 50,
         'cgpa': 5, 'learning_hours': 0, 'online_courses': 0, 'projects': 0},
    ])

    labels = generate_support_risk_labels(factors)

    assert labels.tolist() == ['Low Risk', 'Medium Risk', 'High Risk']
