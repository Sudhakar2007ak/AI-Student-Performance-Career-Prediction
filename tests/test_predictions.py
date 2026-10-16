from types import SimpleNamespace

import pytest

from src.prediction import format_prediction_result, load_model_artifacts
from src.prediction import model_input


def test_format_prediction_result_contains_key_fields():
    result = format_prediction_result({
        'predicted_percentage': 84.5,
        'performance_category': 'Good',
        'career_prediction': 'Data Scientist',
        'career_probabilities': {'Data Scientist': 0.7, 'AI/ML Engineer': 0.2},
        'support_risk': 'Low Risk',
    })
    assert result['predicted_percentage'] == 84.5
    assert result['performance_category'] == 'Good'
    assert result['career_prediction'] == 'Data Scientist'
    assert 'career_probabilities' in result


def test_load_model_artifacts_returns_dictionary():
    artifacts = load_model_artifacts()
    assert isinstance(artifacts, dict)


def test_model_input_uses_trained_feature_order():
    model = SimpleNamespace(feature_names_in_=['external_marks', 'attendance'])
    frame = model_input({'attendance': 88, 'external_marks': 79, 'unused': 1}, model)

    assert list(frame.columns) == ['external_marks', 'attendance']
    assert frame.iloc[0].tolist() == [79, 88]


def test_model_input_reports_missing_trained_features():
    model = SimpleNamespace(feature_names_in_=['internal_marks'])

    with pytest.raises(ValueError, match='internal_marks'):
        model_input({'attendance': 88}, model)
