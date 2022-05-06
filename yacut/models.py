from datetime import datetime

from flask import url_for

from . import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(200))
    short = db.Column(db.String(6), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('short_view', custom_id=self.short, _external=True)
        )

    def to_dict_only_url(self):
        return dict(
            url=self.original
        )
