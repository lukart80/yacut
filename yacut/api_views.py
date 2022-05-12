import re

from flask import request, jsonify

from . import (app, db, NO_BODY_RESPONSE, URL_FIELD_REQUIRED,
               SHORT_URL_EXISTS, INCORRECT_SHORT_URL, ID_NOT_FOUND)
from .exceptions import ApiUsageException
from .models import URL_map
from .views import get_unique_short_id

SHORT_URL_PATTERN = '^[A-Za-z0-9]*$'


@app.route('/api/id/', methods=['POST'])
def create_short_url_api():
    data = request.get_json()
    if data is None:
        raise ApiUsageException(NO_BODY_RESPONSE)
    if 'url' not in data:
        raise ApiUsageException(URL_FIELD_REQUIRED)
    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > 16:
            raise ApiUsageException(INCORRECT_SHORT_URL)
        if URL_map.query.filter_by(short=custom_id).first():
            raise ApiUsageException(SHORT_URL_EXISTS.format(custom_id))
        if not re.match(SHORT_URL_PATTERN, custom_id):
            raise ApiUsageException(INCORRECT_SHORT_URL)
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
        raise ApiUsageException(ID_NOT_FOUND, 404)
    return jsonify(url_map.to_dict_only_url()), 200
