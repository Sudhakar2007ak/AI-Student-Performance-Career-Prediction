from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_preprocessing import SUPPORT_RISK_FEATURES, VALID_RISK_LEVELS, clean_student_data, generate_support_risk_labels

DATA_PATH = Path(__file__).resolve().parent.parent / 'data' / 'student_data.csv'
MODEL_PATH = Path(__file__).resolve().parent.parent / 'models' / 'support_risk_model.pkl'


def train_support_risk_model() -> dict:
    df = pd.read_csv(DATA_PATH)
    df = clean_student_data(df)
    df['support_risk'] = generate_support_risk_labels(df)

    features = [
        'attendance', 'previous_marks', 'assignment_score', 'internal_marks', 'external_marks',
        'cgpa', 'learning_hours', 'online_courses', 'hackathon', 'projects', 'certifications'
    ]
    target = 'support_risk'

    X = df[features]
    y = df[target]
    class_distribution = y.value_counts().reindex(VALID_RISK_LEVELS, fill_value=0)
    print('Support-risk class distribution:')
    for risk, count in class_distribution.items():
        print(f'{risk}: {count}')
    if y.nunique() < 3 or (class_distribution == 0).any():
        raise ValueError(
            'Support-risk training data must contain Low Risk, Medium Risk and High Risk classes.'
        )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('classifier', RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')),
    ])
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    classes = list(model.classes_)

    metrics = {
        'Accuracy': accuracy_score(y_test, predictions),
        'Precision': precision_score(y_test, predictions, average='weighted', zero_division=0),
        'Recall': recall_score(y_test, predictions, average='weighted', zero_division=0),
        'F1': f1_score(y_test, predictions, average='weighted', zero_division=0),
        'ConfusionMatrix': confusion_matrix(y_test, predictions, labels=classes),
        'Classes': classes,
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump({
        'feature_names': features,
        'classes': classes,
    }, Path(__file__).resolve().parent.parent / 'models' / 'preprocessors.pkl')
    return metrics


if __name__ == '__main__':
    metrics = train_support_risk_model()
    print('Support risk model trained successfully.')
    print(f"Classes: {metrics['Classes']}")
    print(f"Accuracy: {metrics['Accuracy']:.4f}")
    print(f"Precision: {metrics['Precision']:.4f}")
    print(f"Recall: {metrics['Recall']:.4f}")
    print(f"F1-score: {metrics['F1']:.4f}")
    print('Confusion matrix:')
    print(metrics['ConfusionMatrix'])
