from flask import Flask
from .models import db
from .main import url_shortener_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(url_shortener_blueprint)

    with app.app_context():
        db.create_all()

    return app