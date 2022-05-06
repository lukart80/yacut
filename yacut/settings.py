import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY')
