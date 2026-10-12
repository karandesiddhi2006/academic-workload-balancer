import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "local-dev-key-change-this"

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///academic_workload.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False