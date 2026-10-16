from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import joblib
import pandas as pd

from src.utils import MODELS_DIR


MODEL_FILES = {
    'performance': MODELS_DIR / 'performance_model.pkl',
    'career': MODELS_DIR / 'career_model.pkl',
    'risk': MODELS_DIR / 'support_risk_model.pkl',
    'preprocessors': MODELS_DIR / 'preprocessors.pkl',
}

FEATURE_COLUMNS = [
    'attendance', 'previous_marks', 'assignment_score', 'internal_marks', 'external_marks',
    'cgpa', 'coding_skill', 'communication_skill', 'problem_solving_skill', 'projects',
    'certifications', 'learning_hours', 'internship', 'online_courses', 'hackathon',
]


def load_model_artifacts() -> Dict[str, Any]:
    artifacts = {}
    for key, path in MODEL_FILES.items():
        if path.exists():
            try:
                artifacts[key] = joblib.load(path)
            except Exception as exc:
                raise RuntimeError(f'Could not load model artifact {path}: {exc}') from exc
    return artifacts


def ensure_model_present(model_name: str) -> None:
    path = MODEL_FILES.get(model_name)
    if path is None or not path.exists():
        expected_path = path if path is not None else MODELS_DIR / f'{model_name}.pkl'
        raise FileNotFoundError(f'Required model file is missing: {expected_path}')


def load_model(model_name: str) -> Any:
    ensure_model_present(model_name)
    path = MODEL_FILES[model_name]
    try:
        return joblib.load(path)
    except Exception as exc:
        raise RuntimeError(f'Could not load model file {path}: {exc}') from exc


def model_input(record: Dict[str, Any] | pd.DataFrame, model: Any) -> pd.DataFrame:
    frame = record.copy() if isinstance(record, pd.DataFrame) else pd.DataFrame([record])
    feature_names = list(getattr(model, 'feature_names_in_', FEATURE_COLUMNS))
    missing_features = [feature for feature in feature_names if feature not in frame.columns]
    if missing_features:
        raise ValueError(f'Missing model input features: {", ".join(missing_features)}')
    ordered = frame.loc[:, feature_names].copy()
    for feature in feature_names:
        ordered[feature] = pd.to_numeric(ordered[feature], errors='coerce')
    return ordered


def predict_performance(record: Dict[str, Any]) -> float:
    model = load_model('performance')
    prediction = model.predict(model_input(record, model))[0]
    return float(prediction)


def predict_career(record: Dict[str, Any]) -> tuple[str, Dict[str, float]]:
    model = load_model('career')
    features = model_input(record, model)
    career = str(model.predict(features)[0])
    probabilities: Dict[str, float] = {}
    if hasattr(model, 'predict_proba'):
        values = model.predict_proba(features)[0]
        probabilities = {
            str(label): float(probability)
            for label, probability in zip(model.classes_, values)
        }
    return career, probabilities


def predict_support_risk(record: Dict[str, Any]) -> str:
    model = load_model('risk')
    if set(getattr(model, 'classes_', [])) != {'Low Risk', 'Medium Risk', 'High Risk'}:
        raise RuntimeError(
            'The saved support-risk model must be retrained with Low Risk, Medium Risk, and High Risk classes.'
        )
    return str(model.predict(model_input(record, model))[0])


def format_prediction_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'predicted_percentage': payload.get('predicted_percentage'),
        'performance_category': payload.get('performance_category', 'Unavailable'),
        'career_prediction': payload.get('career_prediction', 'Unavailable'),
        'career_probabilities': payload.get('career_probabilities', {}),
        'support_risk': payload.get('support_risk', 'Unavailable'),
    }


def predict_student_profile(student_record: Dict[str, Any]) -> Dict[str, Any]:
    percentage = predict_performance(student_record)
    career, career_probabilities = predict_career(student_record)
    support_risk = predict_support_risk(student_record)
    if support_risk not in ['Low Risk', 'Medium Risk', 'High Risk']:
        support_risk = 'Medium Risk'

    return {
        'predicted_percentage': round(percentage, 2),
        'performance_category': classify_percentage(percentage),
        'career_prediction': str(career),
        'career_probabilities': career_probabilities,
        'support_risk': support_risk,
    }


def classify_percentage(value: float) -> str:
    if value >= 80:
        return 'Excellent'
    if value >= 70:
        return 'Good'
    if value >= 55:
        return 'Average'
    return 'Needs Improvement'
