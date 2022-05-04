from datetime import datetime

from yacut import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(200))
    short = db.Column(db.String(6), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

