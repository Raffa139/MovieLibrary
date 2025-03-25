from flask import Flask
from repository import db
import repository.entities
from .config import Config
from .routes import bp as main


def create_app(flask_config=Config):
    app = Flask(__name__,
                template_folder=flask_config.TEMPLATE_FOLDER,
                static_folder=flask_config.STATIC_FOLDER)
    app.config.from_object(flask_config)

    app.register_blueprint(main)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
