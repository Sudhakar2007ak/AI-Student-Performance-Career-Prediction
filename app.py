import streamlit as st

from pages import admin_dashboard, career_prediction, dashboard, skill_recommendation, student_prediction
from src.utils import load_environment

st.set_page_config(page_title='AI Student Career Prediction', page_icon='🎓', layout='wide')

load_environment()


def render_home() -> None:
    st.title('AI-Powered Student Performance & Career Prediction System')
    st.markdown('''
    ## Welcome

    This system estimates academic performance, explores career domains, highlights skill gaps,
    and presents student analytics using the project’s trained machine-learning models.

    ### Modules
    - Student profiles and performance prediction
    - Career estimates and skill-gap recommendations
    - Academic support guidance and analytics
    - Administrator reporting

    > Predictions are estimates generated from available input data and should be used as guidance rather than as a definitive judgment.
    ''')
    st.info('Choose a module from the sidebar to begin.')

pages = {
    'Home': [
        st.Page(render_home, title='Home', url_path='home', default=True),
    ],
    'Student': [
        st.Page(dashboard.render_profile_page, title='Student Profile', url_path='student-profile'),
        st.Page(student_prediction.render_page, title='Performance Prediction', url_path='performance-prediction'),
        st.Page(career_prediction.render_page, title='Career Prediction', url_path='career-prediction'),
        st.Page(skill_recommendation.render_page, title='Skill Recommendations', url_path='skill-recommendations'),
        st.Page(dashboard.render_support_info, title='Academic Support', url_path='academic-support'),
    ],
    'Insights': [
        st.Page(dashboard.render_page, title='Academic Dashboard', url_path='academic-dashboard'),
        st.Page(dashboard.render_analytics, title='Analytics', url_path='analytics'),
    ],
    'Administration': [
        st.Page(admin_dashboard.render_page, title='Admin Dashboard', url_path='admin-dashboard'),
    ],
}

navigation = st.navigation(pages, position='sidebar')
navigation.run()
