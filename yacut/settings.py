import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SECRET_KEY = os.getenv('SECRET_KEY')
