from environment import database_uri
from definitions import TEMPLATES_DIR, STATIC_DIR


class Config:
    SQLALCHEMY_DATABASE_URI = database_uri()
    TEMPLATE_FOLDER = TEMPLATES_DIR
    STATIC_FOLDER = STATIC_DIR
