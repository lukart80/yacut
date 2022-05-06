import re

from flask import request, jsonify, url_for

from . import app, db
from .exceptions import ApiUsageException
from .models import URL_map
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_url_api():
    data = request.get_json()
    if data is None:
        raise ApiUsageException('Отсутствует тело запроса')
    if 'url' not in data:
        raise ApiUsageException('"url" является обязательным полем!')
    custom_id = data.get('short')
    if custom_id:
        if len(custom_id) > 16:
            raise ApiUsageException('Указано недопустимое имя для короткой ссылки')
        if URL_map.query.filter_by(short=custom_id).first():
            raise ApiUsageException(f'Имя "{custom_id}" уже занято.')
        if not re.match('^[A-Za-z0-9]*$', custom_id):
            raise ApiUsageException('Указано недопустимое имя для короткой ссылки')
    if not custom_id:
        custom_id = get_unique_short_id()
    url_map = URL_map(
        original=data.get('url'),
        short=custom_id
    )
    db.session.add(url_map)
    db.session.commit()

    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short>/')
def get_full_url_api(short):
    url_map = URL_map.query.filter_by(short=short).first()
    if not url_map:
        raise ApiUsageException('Указанный id не найден', 404)
    return jsonify(url_map.to_dict_only_url()), 200
