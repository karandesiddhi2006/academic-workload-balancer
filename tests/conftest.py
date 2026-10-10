
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def app(tmp_path):
    from app import create_app, db

    test_db_path = tmp_path / "test_academic_workload.db"

    application = create_app()
    application.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{test_db_path.as_posix()}",
        WTF_CSRF_ENABLED=False,
    )

    # Reconnect SQLAlchemy to an isolated test database.
    db.engine.dispose()

    with application.app_context():
        db.drop_all()
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


@pytest.fixture
def db(app):
    from app import db as database
    return database

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def app(tmp_path):
    from flask import Flask
    from app import db
    from config.config import Config

    test_db_path = tmp_path / "test_academic_workload.db"

    application = Flask(__name__)
    application.config.from_object(Config)
    application.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{test_db_path.as_posix()}",
        WTF_CSRF_ENABLED=False,
    )

    db.init_app(application)

    with application.app_context():
        from app import models
        db.create_all()

        yield application

        db.session.remove()
        db.drop_all()


@pytest.fixture
def db(app):
    from app import db as database
    return database
