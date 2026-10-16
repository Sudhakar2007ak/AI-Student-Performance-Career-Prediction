from src.recommendations import get_skill_recommendations, map_career_to_skills


def test_map_career_to_skills_returns_list():
    skills = map_career_to_skills('Data Scientist')
    assert isinstance(skills, list)
    assert len(skills) > 0


def test_get_skill_recommendations_returns_relevant_skills():
    recs = get_skill_recommendations('Data Scientist', ['Python', 'SQL'])
    assert 'Pandas' in recs
    assert 'Python' not in recs
    assert isinstance(recs, list)
