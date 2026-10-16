import pytest

from src.database import DatabaseConfigurationError, get_connection
from src import utils


def test_get_connection_requires_mysql_password(monkeypatch, tmp_path):
    monkeypatch.setattr(utils, 'ROOT_DIR', tmp_path)
    for key in ['MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE']:
        monkeypatch.delenv(key, raising=False)

    with pytest.raises(DatabaseConfigurationError, match='MYSQL_PASSWORD'):
        get_connection()


def test_mysql_config_loads_project_root_dotenv(monkeypatch, tmp_path):
    monkeypatch.setattr(utils, 'ROOT_DIR', tmp_path)
    for key in ['MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE']:
        monkeypatch.delenv(key, raising=False)
    (tmp_path / '.env').write_text(
        'MYSQL_HOST=db.example.test\n'
        'MYSQL_PORT=3307\n'
        'MYSQL_USER=student_app\n'
        'MYSQL_PASSWORD=test-only-placeholder\n'
        'MYSQL_DATABASE=student_career_prediction\n',
        encoding='utf-8',
    )

    config = utils.get_mysql_config()

    assert config['host'] == 'db.example.test'
    assert config['port'] == 3307
    assert config['user'] == 'student_app'
    assert config['password'] == 'test-only-placeholder'
    assert config['database'] == 'student_career_prediction'