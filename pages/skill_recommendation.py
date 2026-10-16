from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.recommendations import CAREER_SKILLS, map_career_to_skills


def render_page() -> None:
    st.title('Skill Recommendations')
    st.write('Compare your current skills with the requirements of a career you are exploring.')

    career = st.selectbox('Career interest', list(CAREER_SKILLS))
    required_skills = map_career_to_skills(career)
    all_skills = sorted({skill for skills in CAREER_SKILLS.values() for skill in skills})
    technical_skills = st.multiselect('Current technical skills', all_skills)
    programming_skills = st.multiselect(
        'Programming skills', ['Python', 'Java', 'JavaScript', 'C', 'C++', 'C#', 'SQL', 'R', 'Go'],
    )
    skill_level = st.select_slider('Current skill level', options=['Beginner', 'Intermediate', 'Advanced'])

    current_skills = list(dict.fromkeys(technical_skills + programming_skills))
    current_lower = {skill.lower() for skill in current_skills}
    missing_skills = [skill for skill in required_skills if skill.lower() not in current_lower]
    matched_skills = [skill for skill in required_skills if skill.lower() in current_lower]

    if skill_level == 'Beginner':
        priorities = ['High Priority'] * len(missing_skills)
    elif skill_level == 'Intermediate':
        priorities = ['High Priority' if index < 3 else 'Medium Priority' for index in range(len(missing_skills))]
    else:
        priorities = ['Medium Priority' if index < 2 else 'Low Priority' for index in range(len(missing_skills))]

    st.subheader(f'Skill gap for {career}')
    current_col, recommended_col = st.columns(2)
    with current_col:
        st.markdown('#### CURRENT SKILLS')
        st.write(', '.join(current_skills) if current_skills else 'No skills selected yet.')
        st.metric('Matching requirements', f'{len(matched_skills)} / {len(required_skills)}')
    with recommended_col:
        st.markdown('#### RECOMMENDED SKILLS')
        st.write(', '.join(required_skills))
        st.metric('Missing skills', len(missing_skills))

    if missing_skills:
        gap_frame = pd.DataFrame({'Missing skill': missing_skills, 'Learning priority': priorities})
        st.dataframe(gap_frame, hide_index=True, use_container_width=True)
    else:
        st.success('Your selected skills cover all requirements in this career map.')

    chart_frame = pd.DataFrame({
        'Skill status': ['Current match', 'To develop'],
        'Skills': [len(matched_skills), len(missing_skills)],
    })
    figure = px.bar(
        chart_frame,
        x='Skill status',
        y='Skills',
        color='Skill status',
        title='Current skills vs career requirements',
        color_discrete_map={'Current match': '#45b8ac', 'To develop': '#f2a65a'},
    )
    st.plotly_chart(figure, use_container_width=True)
