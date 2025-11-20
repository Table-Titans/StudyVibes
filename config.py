import os
from urllib.parse import quote_plus
import dotenv


class Config:

    dotenv.load_dotenv()

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    host = os.getenv("DATABASE_HOST")
    user = os.getenv("DATABASE_USER")
    pwd_raw = os.getenv("DATABASE_PASSWORD")
    port = os.getenv("DATABASE_PORT", "3306")
    name = os.getenv("DATABASE_NAME")

    if host and user and pwd_raw and name:
        pwd = quote_plus(pwd_raw)
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{name}"
        )
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 280, "pool_pre_ping": True}
    else:
        # HANDLE ERROR WHEN DB CREDENTIALS ARE MISSING
        raise ValueError(
            "Database configuration is incomplete. Please set all required environment variables."
        )
