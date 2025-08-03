from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class URLMap(db.Model):
    __tablename__ = 'url_map'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    click_count = db.Column(db.Integer, default=0)

    def __init__(self, original_url, short_code):
        self.original_url = original_url
        self.short_code = short_code