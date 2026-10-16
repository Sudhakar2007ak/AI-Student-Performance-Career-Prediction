from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard_data import add_model_outputs, load_student_records


def render_page() -> None:
    st.title('Admin Dashboard')
    records, source, database_message = load_student_records()
    if source == 'demo dataset':
        if database_message and not database_message.startswith('The database is reachable'):
            st.warning('MySQL is unavailable. The dashboard is currently using the project dataset.')
            st.info(
                'Copy .env.example to .env in the project root, then set '
                'MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE. '
            )
        else:
            st.info(database_message or 'No MySQL records are available; showing the project dataset.')
    elif source == 'unavailable':
        st.warning('MySQL is unavailable and no fallback dataset exists.')
        st.info(
            'Configure MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE '
            'in a project-root .env file copied from .env.example. No fallback dataset is available.'
        )
        return

    if records.empty:
        st.info('No database records or dataset rows are available yet.')
        return

    records, model_errors = add_model_outputs(records)
    for model_name, error in model_errors.items():
        if model_name == 'risk':
            st.error(f'Support-risk model is unavailable. {error}')
        else:
            st.warning(f'A dashboard model output is unavailable: {error}')

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    departments = sorted(records['department'].dropna().astype(str).unique())
    semesters = sorted(records['semester'].dropna().unique().tolist())
    risks = sorted(records['support_risk'].dropna().astype(str).unique())
    department_filter = filter_col1.selectbox('Department', ['All'] + departments)
    semester_filter = filter_col2.selectbox('Semester', ['All'] + semesters)
    risk_filter = filter_col3.selectbox('Support risk', ['All'] + risks)

    filtered = records.copy()
    if department_filter != 'All':
        filtered = filtered[filtered['department'].astype(str) == department_filter]
    if semester_filter != 'All':
        filtered = filtered[filtered['semester'] == semester_filter]
    if risk_filter != 'All':
        filtered = filtered[filtered['support_risk'].astype(str) == risk_filter]

    predicted_values = pd.to_numeric(filtered['predicted_percentage'], errors='coerce')
    support_count = (
        int((filtered['support_risk'].astype(str) == 'High Risk').sum())
        if filtered['support_risk'].notna().any()
        else 'N/A'
    )
    metrics = st.columns(5)
    metrics[0].metric('Total students', len(filtered))
    metrics[1].metric('Average CGPA', f"{filtered['cgpa'].mean():.2f}" if 'cgpa' in filtered and filtered['cgpa'].notna().any() else 'N/A')
    metrics[2].metric('Average attendance', f"{filtered['attendance'].mean():.1f}%" if 'attendance' in filtered and filtered['attendance'].notna().any() else 'N/A')
    metrics[3].metric('Average predicted percentage', f'{predicted_values.mean():.2f}%' if predicted_values.notna().any() else 'N/A')
    metrics[4].metric('Students requiring support', support_count)

    if filtered.empty:
        st.info('No students match the selected filters.')
        return

    performance_frame = filtered.assign(_predicted=pd.to_numeric(filtered['predicted_percentage'], errors='coerce'))
    career_column = 'career_prediction' if filtered['career_prediction'].notna().any() else 'career_domain'
    charts_col1, charts_col2 = st.columns(2)
    charts_col1.plotly_chart(
        px.histogram(performance_frame, x='_predicted', nbins=15, title='Performance distribution', labels={'_predicted': 'Predicted percentage'}),
        use_container_width=True,
    )
    if career_column in filtered.columns:
        charts_col2.plotly_chart(px.histogram(filtered, x=career_column, title='Career prediction distribution'), use_container_width=True)
    charts_col1.plotly_chart(
        px.histogram(filtered, x='attendance', nbins=15, title='Attendance distribution'),
        use_container_width=True,
    )
    charts_col2.plotly_chart(px.histogram(filtered, x='support_risk', title='Support risk distribution'), use_container_width=True)

    st.subheader('Student records')
    st.dataframe(filtered, hide_index=True, use_container_width=True)
