from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT_DIR / 'models'
DATA_DIR = ROOT_DIR / 'data'


def load_environment() -> None:
    load_dotenv(dotenv_path=ROOT_DIR / '.env')


def get_mysql_config() -> dict:
    load_environment()
    return {
        'host': os.getenv('MYSQL_HOST') or 'localhost',
        'port': int(os.getenv('MYSQL_PORT') or '3306'),
        'user': os.getenv('MYSQL_USER') or 'root',
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_DATABASE') or 'student_career_prediction',
    }
