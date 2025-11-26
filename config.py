import os
from urllib.parse import quote_plus
import dotenv
import socket


class Config:

    dotenv.load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    host = os.getenv("DATABASE_HOST")
    user = os.getenv("DATABASE_USER")
    pwd_raw = os.getenv("DATABASE_PASSWORD")
    port = os.getenv("DATABASE_PORT", "3306")
    name = os.getenv("DATABASE_NAME")
    pwd = quote_plus(pwd_raw) if pwd_raw else ""
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{name}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 280, "pool_pre_ping": True}

    # Simple host resolution log to help debug DB connectivity in worker/cron
    try:
        resolved_ip = socket.gethostbyname(host) if host else "no host"
        print(f"DB host: {host}, resolved_ip: {resolved_ip}, port: {port}")
    except Exception:
        print(f"DB host: {host}, resolved_ip: unresolved, port: {port}")
