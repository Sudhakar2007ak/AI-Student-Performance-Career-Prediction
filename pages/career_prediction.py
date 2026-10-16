from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_preprocessing import validate_student_record
from src.prediction import predict_career
from src.recommendations import map_career_to_skills


def render_page() -> None:
    st.title('Career Prediction')
    st.write('Explore career domains estimated from academic performance and skill indicators.')
    with st.form('career_prediction_form'):
        academic_col, skill_col = st.columns(2)
        with academic_col:
            attendance = st.number_input('Attendance (%)', 0, 100, 0)
            previous_marks = st.number_input('Previous marks (%)', 0, 100, 0)
            assignment_score = st.number_input('Assignment score (%)', 0, 100, 0)
            internal_marks = st.number_input('Internal marks (%)', 0, 100, 0)
            external_marks = st.number_input('External marks (%)', 0, 100, 0)
            cgpa = st.number_input('CGPA', 0.0, 10.0, 0.0, step=0.1)
            learning_hours = st.number_input('Learning hours per week', 0, 80, 0)
        with skill_col:
            coding_skill = st.slider('Coding skill (1-10)', 1, 10, 1)
            communication_skill = st.slider('Communication skill (1-10)', 1, 10, 1)
            problem_solving_skill = st.slider('Problem-solving skill (1-10)', 1, 10, 1)
            projects = st.number_input('Projects', 0, 20, 0)
            certifications = st.number_input('Certifications', 0, 20, 0)
            internship = st.number_input('Internship experience', 0, 2, 0)
            online_courses = st.number_input('Online courses', 0, 50, 0)
            hackathon = st.number_input('Hackathon participation', 0, 20, 0)
        submitted = st.form_submit_button('Predict Career', type='primary')

    if not submitted:
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
        career, probabilities = predict_career(features)
    except Exception as exc:
        st.error(f'Career prediction failed: {exc}')
        return

    st.success(f'Predicted career domain: {career}')
    if probabilities:
        probability_frame = pd.DataFrame(
            [{'Career domain': name, 'Probability': value} for name, value in probabilities.items()]
        ).sort_values('Probability', ascending=False)
        st.subheader('Top career domains')
        st.dataframe(probability_frame.head(3), hide_index=True, use_container_width=True)
        figure = px.bar(
            probability_frame.head(10),
            x='Probability',
            y='Career domain',
            orientation='h',
            title='Career model probabilities',
            range_x=[0, 1],
        )
        figure.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(figure, use_container_width=True)
    else:
        st.info('This trained model does not provide predict_proba; only its predicted career is available.')

    st.subheader(f'Skills associated with {career}')
    st.write(', '.join(map_career_to_skills(career)))
