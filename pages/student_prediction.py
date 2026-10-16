from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_preprocessing import validate_student_record
from src.prediction import classify_percentage, predict_performance


def render_page() -> None:
    st.title('Performance Prediction')
    st.write('Enter a student profile to estimate final academic performance with the trained model.')

    with st.form('student_performance_prediction'):
        identity_col, academic_col, skill_col = st.columns(3)
        with identity_col:
            student_id = st.text_input('Student ID', placeholder='e.g. STU-1042')
            student_name = st.text_input('Student name')
            department = st.selectbox('Department', [
                'Computer Science', 'Information Technology', 'Electronics', 'Mechanical',
                'Civil', 'Business', 'Other',
            ])
            semester = st.number_input('Semester', min_value=1, max_value=12, value=1)
            cgpa = st.number_input('CGPA', min_value=0.0, max_value=10.0, value=0.0, step=0.1)
            attendance = st.number_input('Attendance (%)', min_value=0, max_value=100, value=0)
        with academic_col:
            previous_marks = st.number_input('Previous marks (%)', min_value=0, max_value=100, value=0)
            assignment_score = st.number_input('Assignment score (%)', min_value=0, max_value=100, value=0)
            internal_marks = st.number_input('Internal marks (%)', min_value=0, max_value=100, value=0)
            external_marks = st.number_input('External marks (%)', min_value=0, max_value=100, value=0)
            projects = st.number_input('Number of projects', min_value=0, max_value=20, value=0)
            certifications = st.number_input('Certifications', min_value=0, max_value=20, value=0)
        with skill_col:
            coding_skill = st.slider('Coding skill (1-10)', min_value=1, max_value=10, value=1)
            communication_skill = st.slider('Communication skill (1-10)', min_value=1, max_value=10, value=1)
            problem_solving_skill = st.slider('Problem-solving skill (1-10)', min_value=1, max_value=10, value=1)
            learning_hours = st.number_input('Learning hours per week', min_value=0, max_value=80, value=0)
            internship = st.number_input('Internship experience', min_value=0, max_value=2, value=0)
            online_courses = st.number_input('Online courses completed', min_value=0, max_value=50, value=0)
            hackathon = st.number_input('Hackathon participation', min_value=0, max_value=20, value=0)
        submitted = st.form_submit_button('Predict Performance', type='primary')

    if not submitted:
        return
    if not student_id.strip() or not student_name.strip():
        st.error('Enter both a student ID and student name before predicting.')
        return

    features = {
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
    }
    if not validate_student_record(features):
        st.error('Some academic or skill values are outside the valid range. Review the form and try again.')
        return

    try:
        percentage = predict_performance(features)
    except Exception as exc:
        st.error(f'Performance prediction failed: {exc}')
        return

    category = classify_percentage(percentage)
    st.success(f'Prediction generated for {student_name.strip()} ({student_id.strip()}).')
    result_col, category_col, context_col = st.columns(3)
    result_col.metric('Predicted final percentage', f'{percentage:.2f}%')
    category_col.metric('Performance category', category)
    context_col.metric('Department / semester', f'{department} / {semester}')

    chart_data = pd.DataFrame({
        'Measure': ['Previous marks', 'Assignments', 'Internal marks', 'External marks', 'Predicted final'],
        'Percentage': [previous_marks, assignment_score, internal_marks, external_marks, percentage],
        'Type': ['Input'] * 4 + ['Model prediction'],
    })
    figure = px.bar(
        chart_data,
        x='Measure',
        y='Percentage',
        color='Type',
        range_y=[0, 100],
        title='Academic inputs and model estimate',
        color_discrete_map={'Input': '#45b8ac', 'Model prediction': '#f2a65a'},
    )
    st.plotly_chart(figure, use_container_width=True)