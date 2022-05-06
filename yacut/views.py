import random
import string

from flask import render_template, flash, redirect, abort

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
        custom_id = form.short.data
        if URL_map.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('create_link.html', form=form)

        if not custom_id:
            custom_id = get_unique_short_id()
        url_map = URL_map(
            original=form.original.data,
            short=custom_id
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template('create_link.html', form=form, custom_id=custom_id), 200

    return render_template('create_link.html', form=form)


@app.route('/<string:custom_id>')
def short_view(custom_id):
    url_map = URL_map.query.filter_by(short=custom_id).first()
    if not url_map:
        abort(404)
    return redirect(url_map.original)
