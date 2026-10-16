from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_preprocessing import clean_student_data

DATA_PATH = Path(__file__).resolve().parent.parent / 'data' / 'student_data.csv'
MODEL_PATH = Path(__file__).resolve().parent.parent / 'models' / 'career_model.pkl'


def train_career_model() -> dict:
    df = pd.read_csv(DATA_PATH)
    df = clean_student_data(df)

    features = [
        'attendance', 'previous_marks', 'assignment_score', 'internal_marks', 'external_marks',
        'cgpa', 'coding_skill', 'communication_skill', 'problem_solving_skill',
        'projects', 'certifications', 'learning_hours', 'internship', 'online_courses', 'hackathon'
    ]
    target = 'career_domain'

    df = df.dropna(subset=[target])
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=250, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    metrics = {
        'Accuracy': accuracy_score(y_test, predictions),
        'Precision': precision_score(y_test, predictions, average='weighted', zero_division=0),
        'Recall': recall_score(y_test, predictions, average='weighted', zero_division=0),
        'F1': f1_score(y_test, predictions, average='weighted', zero_division=0),
        'ConfusionMatrix': confusion_matrix(y_test, predictions),
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump({
        'feature_names': [
            'attendance', 'previous_marks', 'assignment_score', 'internal_marks', 'external_marks',
            'cgpa', 'coding_skill', 'communication_skill', 'problem_solving_skill',
            'projects', 'certifications', 'learning_hours', 'internship', 'online_courses', 'hackathon'
        ],
        'classes': list(model.classes_)
    }, Path(__file__).resolve().parent.parent / 'models' / 'preprocessors.pkl')
    return metrics


if __name__ == '__main__':
    metrics = train_career_model()
    print('Career model trained successfully.')
    print(metrics)
