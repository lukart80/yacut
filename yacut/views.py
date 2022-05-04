import random
import string

from flask import render_template, flash, url_for

from . import app, db
from .forms import UriForm
from .models import URL_map


def get_unique_short_id():
    short = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    while URL_map.query.filter_by(short=short).first():
        short = ''.join(
            random.choices(string.ascii_letters + string.digits, k=6))
    return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UriForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if URL_map.query.filter_by(short=short).first():
            flash(f'"Имя {short} уже занято!')
            return render_template('create_link.html', form=form)

        if not short:
            short = get_unique_short_id()
        url_map = URL_map(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template('create_link.html', form=form, short=short)

    return render_template('create_link.html', form=form)


@app.route('/<string:short>')
def short_view(short):
    return short