from flask import render_template, jsonify

from . import app
from .exceptions import ApiUsageException


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


@app.errorhandler(ApiUsageException)
def api_exception(exception):
    response = dict(
        message=exception.message
    )
    return jsonify(response), exception.status_code
