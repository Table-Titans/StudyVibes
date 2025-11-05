import os
import dotenv


class Config:

    dotenv.load_dotenv()

    host = os.getenv("DATABASE_HOST")
    user = os.getenv("DATABASE_USER")
    pwd = os.getenv("DATABASE_PASSWORD")
    port = os.getenv("DATABASE_PORT")
    name = os.getenv("DATABASE_NAME")

    if host and user and pwd and name:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{user}:{pwd}@{host}:{str(3306)}/{name}"
        )
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    else:
        # HANDLE ERROR WHEN DB CREDENTIALS ARE MISSING
        raise ValueError(
            "Database configuration is incomplete. Please set all required environment variables."
        )
