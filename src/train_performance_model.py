from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_preprocessing import clean_student_data

DATA_PATH = Path(__file__).resolve().parent.parent / 'data' / 'student_data.csv'
MODEL_PATH = Path(__file__).resolve().parent.parent / 'models' / 'performance_model.pkl'


def train_performance_model() -> dict:
    df = pd.read_csv(DATA_PATH)
    df = clean_student_data(df)

    features = [
        'attendance', 'previous_marks', 'assignment_score', 'internal_marks', 'external_marks',
        'cgpa', 'coding_skill', 'communication_skill', 'problem_solving_skill',
        'projects', 'certifications', 'learning_hours', 'internship', 'online_courses', 'hackathon'
    ]
    target = 'final_percentage'

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    metrics = {
        'MAE': mean_absolute_error(y_test, predictions),
        'MSE': mean_squared_error(y_test, predictions),
        'RMSE': __import__('numpy').sqrt(mean_squared_error(y_test, predictions)),
        'R2': r2_score(y_test, predictions),
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump({
        'feature_names': [
            'attendance', 'previous_marks', 'assignment_score', 'internal_marks', 'external_marks',
            'cgpa', 'coding_skill', 'communication_skill', 'problem_solving_skill',
            'projects', 'certifications', 'learning_hours', 'internship', 'online_courses', 'hackathon'
        ]
    }, Path(__file__).resolve().parent.parent / 'models' / 'preprocessors.pkl')
    return metrics


if __name__ == '__main__':
    metrics = train_performance_model()
    print('Performance model trained successfully.')
    print(metrics)
