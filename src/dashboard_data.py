from __future__ import annotations

from typing import Any

import pandas as pd

from src.database import fetch_student_records
from src.prediction import load_model, model_input
from src.utils import DATA_DIR


def load_student_records() -> tuple[pd.DataFrame, str, str | None]:
    database_message = None

    try:
        records = fetch_student_records()

        if records:
            return pd.DataFrame(records), "MySQL database", None

        database_message = (
            "The database is reachable, but it contains no student records."
        )

    except Exception as exc:
        database_message = str(exc)

    dataset_path = DATA_DIR / "student_data.csv"

    if dataset_path.exists():
        return pd.read_csv(dataset_path), "demo dataset", database_message

    return pd.DataFrame(), "unavailable", database_message


def add_model_outputs(
    frame: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, str]]:

    result = frame.copy()
    errors: dict[str, str] = {}

    model_columns = {
        "performance": "predicted_percentage",
        "career": "career_prediction",
        "risk": "support_risk",
    }

    for model_name, output_column in model_columns.items():

        if output_column not in result.columns:
            result[output_column] = pd.NA

        if model_name == "risk":
            result[output_column] = pd.NA

        missing = (
            pd.Series(True, index=result.index)
            if model_name == "risk"
            else result[output_column].isna()
        )

        if not missing.any():
            continue

        try:
            model: Any = load_model(model_name)

            if model_name == "risk" and set(
                getattr(model, "classes_", [])
            ) != {
                "Low Risk",
                "Medium Risk",
                "High Risk",
            }:
                raise ValueError(
                    "The saved support-risk model must be retrained "
                    "with Low Risk, Medium Risk, and High Risk classes."
                )

            values = model.predict(
                model_input(result.loc[missing], model)
            )

            result.loc[missing, output_column] = values

        except Exception as exc:
            errors[model_name] = str(exc)

    # Student profile information
    if "student_id" in result.columns:

        if "name" not in result.columns:
            result["name"] = result["student_id"].astype(str)

        if "department" not in result.columns:
            result["department"] = (
                "Artificial Intelligence and Data Science"
            )
        else:
            result["department"] = result["department"].fillna(
                "Artificial Intelligence and Data Science"
            )

        if "semester" not in result.columns:
            result["semester"] = 5
        else:
            result["semester"] = result["semester"].fillna(5)

    if (
        "career_prediction" not in result.columns
        and "career_domain" in result.columns
    ):
        result["career_prediction"] = result["career_domain"]

    return result, errors