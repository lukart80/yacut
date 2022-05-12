from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config

app = Flask(__name__, static_url_path='')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

NO_BODY_RESPONSE = 'Отсутствует тело запроса'
URL_FIELD_REQUIRED = '"url" является обязательным полем!'
INCORRECT_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'
SHORT_URL_EXISTS = 'Имя "{}" уже занято.'
ID_NOT_FOUND = 'Указанный id не найден'

from . import views, models, api_views, error_handlers, exceptions
