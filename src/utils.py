
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT_DIR / "models"
DATA_DIR = ROOT_DIR / "data"


def load_environment() -> None:
    load_dotenv(dotenv_path=ROOT_DIR / ".env")


def get_mysql_config() -> dict:
    load_environment()

    # Local .env / environment variables
    config = {
        "host": os.getenv("MYSQL_HOST") or "localhost",
        "port": int(os.getenv("MYSQL_PORT") or "3306"),
        "user": os.getenv("MYSQL_USER") or "root",
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE")
        or "student_career_prediction",
    }

    # Streamlit Community Cloud Secrets override local defaults
    try:
        import streamlit as st

        secrets = st.secrets
        config["host"] = secrets.get("MYSQL_HOST", config["host"])
        config["port"] = int(
            secrets.get("MYSQL_PORT", config["port"])
        )
        config["user"] = secrets.get("MYSQL_USER", config["user"])
        config["password"] = secrets.get(
            "MYSQL_PASSWORD", config["password"]
        )
        config["database"] = secrets.get(
            "MYSQL_DATABASE", config["database"]
        )
    except Exception:
        # When Streamlit Secrets are unavailable, use local config.
        pass

    return config
