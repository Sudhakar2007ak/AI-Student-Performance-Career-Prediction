from __future__ import annotations

from typing import List


CAREER_SKILLS = {
    'Data Scientist': ['Python', 'Pandas', 'NumPy', 'SQL', 'Statistics', 'Machine Learning', 'Data Visualization', 'Scikit-learn', 'Power BI'],
    'AI/ML Engineer': ['Python', 'Mathematics', 'Statistics', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'NLP', 'Computer Vision', 'MLOps'],
    'Data Analyst': ['Excel', 'SQL', 'Python', 'Pandas', 'Data Visualization', 'Power BI', 'Statistics', 'Dashboarding'],
    'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'REST APIs', 'SQL', 'Git/GitHub'],
    'Software Developer': ['Python', 'Java', 'Data Structures', 'Algorithms', 'Git/GitHub', 'Testing', 'OOP', 'Software Design'],
    'Cybersecurity Analyst': ['Networking', 'Linux', 'Security Tools', 'Ethical Hacking', 'Risk Assessment', 'Python', 'SIEM', 'Cloud Security'],
    'Cloud Engineer': ['Linux', 'AWS', 'Azure', 'Docker', 'Kubernetes', 'Networking', 'Terraform', 'Python'],
    'DevOps Engineer': ['Linux', 'Docker', 'CI/CD', 'Git/GitHub', 'Kubernetes', 'Terraform', 'Cloud Basics', 'Monitoring'],
    'Database Administrator': ['SQL', 'Database Design', 'MySQL', 'Performance Tuning', 'Backup Management', 'Data Modeling', 'Security'],
    'UI/UX Designer': ['Figma', 'UX Research', 'Design Thinking', 'Wireframing', 'Prototyping', 'User Testing', 'HTML', 'CSS'],
}


def map_career_to_skills(career: str) -> List[str]:
    return CAREER_SKILLS.get(career, ['Python', 'Communication', 'Problem Solving'])


def get_skill_recommendations(career: str, current_skills: List[str]) -> List[str]:
    career_skills = map_career_to_skills(career)
    current_lower = {skill.lower() for skill in current_skills}
    recommendations = []
    for skill in career_skills:
        if skill.lower() not in current_lower:
            recommendations.append(skill)
    return recommendations[:8]


def generate_support_actions(risk_level: str) -> List[str]:
    actions = {
        'High Risk': [
            'Meet academic advisor',
            'Increase study hours',
            'Complete pending assignments',
            'Attend additional classes',
            'Practice weak subjects',
        ],
        'Medium Risk': [
            'Improve attendance',
            'Follow a weekly study plan',
            'Practice difficult topics',
            'Review previous assessments',
        ],
        'Low Risk': [
            'Continue current learning pattern',
            'Consider advanced projects and certifications',
            'Explore leadership and mentoring opportunities',
        ],
    }
    return actions.get(risk_level, actions['Medium Risk'])
