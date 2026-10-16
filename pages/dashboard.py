from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard_data import add_model_outputs, load_student_records
from src.prediction import classify_percentage, predict_career
from src.recommendations import generate_support_actions


def _read_dashboard_data() -> pd.DataFrame:
    frame, source, database_message = load_student_records()
    if source == 'demo dataset':
        if database_message and database_message.startswith('The database is reachable'):
            st.info('MySQL is available but has no student records. The dashboard is using the project dataset.')
        else:
            st.warning('MySQL is unavailable. The dashboard is currently using the project dataset.')
            st.info(
                'Configure MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE '
                'in the project-root .env file.'
            )
    elif source == 'unavailable':
        st.warning('No student records are available from MySQL or data/student_data.csv.')
    if database_message and source != 'demo dataset':
        st.warning(f'Database connection unavailable: {database_message}')
    if not frame.empty:
        frame, model_errors = add_model_outputs(frame)
        for model_name, error in model_errors.items():
            if model_name == 'risk':
                st.error(f'Support-risk model is unavailable. {error}')
            else:
                st.warning(f'A dashboard model output is unavailable: {error}')
    return frame


def render_profile_page() -> None:
    st.title('Student Profile')
    records = _read_dashboard_data()
    if records.empty:
        st.info('No database or dataset student records are available to display.')
        return
    ids = records['student_id'].fillna('Unknown').astype(str).tolist()
    selected_id = st.selectbox('Select student', ids)
    student = records.loc[records['student_id'].astype(str) == selected_id].iloc[0]
    st.subheader(str(student.get('name', selected_id)))
    details = st.columns(4)
    details[0].metric('Department', str(student.get('department', 'Not recorded')))
    details[1].metric('Semester', str(student.get('semester', 'Not recorded')))
    details[2].metric('CGPA', f"{float(student['cgpa']):.2f}" if pd.notna(student.get('cgpa')) else 'N/A')
    details[3].metric('Attendance', f"{float(student['attendance']):.1f}%" if pd.notna(student.get('attendance')) else 'N/A')
    profile_data = student.astype(str).to_frame('Value')
    st.dataframe(profile_data, use_container_width=True)


def render_page() -> None:
    st.title('Academic Dashboard')
    records = _read_dashboard_data()
    if records.empty:
        st.info('No database or dataset student records are available for dashboard analytics.')
        return

    if 'student_id' in records.columns:
        student_ids = records['student_id'].fillna('Unknown').astype(str).tolist()
        selected_id = st.selectbox('Student', student_ids, key='academic_dashboard_student')
        selected = records.loc[records['student_id'].astype(str) == selected_id].iloc[0]
    else:
        selected = records.iloc[0]

    predicted = selected.get('predicted_percentage')
    predicted_value = float(predicted) if pd.notna(predicted) else None
    risk = selected.get('support_risk')
    category = classify_percentage(predicted_value) if predicted_value is not None else 'Unavailable'
    metrics = st.columns(4)
    metrics[0].metric('Current CGPA', f"{float(selected['cgpa']):.2f}" if pd.notna(selected.get('cgpa')) else 'N/A')
    metrics[1].metric('Attendance', f"{float(selected['attendance']):.1f}%" if pd.notna(selected.get('attendance')) else 'N/A')
    metrics[2].metric('Previous marks', f"{float(selected['previous_marks']):.1f}%" if pd.notna(selected.get('previous_marks')) else 'N/A')
    metrics[3].metric('Predicted final percentage', f'{predicted_value:.2f}%' if predicted_value is not None else 'Unavailable')

    status = st.columns(3)
    status[0].metric('Performance category', category)
    status[1].metric('Career prediction', str(selected.get('career_prediction', 'Unavailable')))
    status[2].metric('Academic support level', str(risk) if pd.notna(risk) else 'Unavailable')

    plot_data = records.copy()
    plot_data['performance_value'] = pd.to_numeric(plot_data['predicted_percentage'], errors='coerce')
    if 'semester' in plot_data.columns and plot_data['semester'].notna().any():
        marks_trend = plot_data.groupby('semester', as_index=False)['performance_value'].mean()
        trend_figure = px.line(marks_trend, x='semester', y='performance_value', markers=True, title='Marks trend by semester')
    else:
        mark_columns = [column for column in ['previous_marks', 'assignment_score', 'internal_marks', 'external_marks'] if column in plot_data.columns]
        trend_values = plot_data[mark_columns].mean().rename_axis('Assessment').reset_index(name='Average marks')
        trend_figure = px.line(trend_values, x='Assessment', y='Average marks', markers=True, title='Average marks trend')

    attendance_figure = px.scatter(
        plot_data, x='attendance', y='performance_value', color='department' if plot_data['department'].nunique() > 1 else None,
        hover_name='student_id' if 'student_id' in plot_data.columns else None,
        title='Attendance vs predicted performance',
    )
    skill_columns = [column for column in ['coding_skill', 'communication_skill', 'problem_solving_skill'] if column in selected.index]
    skill_data = pd.DataFrame({'Skill': skill_columns, 'Level': [selected[column] for column in skill_columns]})
    skill_figure = px.bar(skill_data, x='Skill', y='Level', range_y=[0, 10], title='Selected student skill distribution')
    learning_figure = px.scatter(
        plot_data, x='learning_hours', y='performance_value',
        hover_name='student_id' if 'student_id' in plot_data.columns else None,
        title='Learning hours vs predicted performance',
    )

    chart_col1, chart_col2 = st.columns(2)
    chart_col1.plotly_chart(trend_figure, use_container_width=True)
    chart_col2.plotly_chart(attendance_figure, use_container_width=True)
    chart_col1.plotly_chart(skill_figure, use_container_width=True)
    chart_col2.plotly_chart(learning_figure, use_container_width=True)

    try:
        career, probabilities = predict_career(selected.to_dict())
        if probabilities:
            probability_frame = pd.DataFrame(
                [{'Career': label, 'Probability': value} for label, value in probabilities.items()]
            ).sort_values('Probability', ascending=False)
            st.plotly_chart(
                px.bar(probability_frame, x='Career', y='Probability', title=f'Career probabilities for {career}'),
                use_container_width=True,
            )
        else:
            st.info('The career model does not expose probability scores.')
    except Exception as exc:
        st.warning(f'Career probability chart is unavailable: {exc}')

    st.caption('Model estimates are guidance and are not definitive judgments of a student or their future.')


def render_support_info() -> None:
    st.title('Academic Support')
    risk = st.selectbox('Select risk level', ['Low Risk', 'Medium Risk', 'High Risk'])
    actions = generate_support_actions(risk)
    st.write(f'Current support category: **{risk}**')
    for action in actions:
        st.markdown(f'- {action}')


def render_analytics() -> None:
    st.title('Analytics')
    records = _read_dashboard_data()
    if records.empty:
        st.info('No student records are available for analytics.')
        return
    records['performance_value'] = pd.to_numeric(records['predicted_percentage'], errors='coerce')
    chart_col1, chart_col2 = st.columns(2)
    chart_col1.plotly_chart(
        px.scatter(records, x='attendance', y='performance_value', color='support_risk', title='Attendance vs performance'),
        use_container_width=True,
    )
    career_column = 'career_prediction' if records['career_prediction'].notna().any() else 'career_domain'
    if career_column in records.columns:
        chart_col2.plotly_chart(px.histogram(records, x=career_column, title='Career prediction distribution'), use_container_width=True)
    chart_col1.plotly_chart(
        px.scatter(records, x='learning_hours', y='performance_value', color='cgpa', title='Learning hours vs performance'),
        use_container_width=True,
    )
    st.dataframe(records, hide_index=True, use_container_width=True)
