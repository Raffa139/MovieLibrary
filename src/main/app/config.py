from environment import database_uri
from definitions import TEMPLATES_DIR, STATIC_DIR, UPLOADS_DIR


class Config:
    SQLALCHEMY_DATABASE_URI = database_uri()
    TEMPLATE_FOLDER = TEMPLATES_DIR
    STATIC_FOLDER = STATIC_DIR
    UPLOADS_FOLDER = UPLOADS_DIR
    ALLOWED_FILE_TYPES = ("png", "jpg", "jpeg", "gif")
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
