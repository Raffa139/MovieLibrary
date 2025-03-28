import os

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCES_DIR = os.path.abspath(os.path.join(MAIN_DIR, os.pardir))
ROOT_DIR = os.path.abspath(os.path.join(SOURCES_DIR, os.pardir))
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
STATIC_DIR = os.path.join(ROOT_DIR, "static")
UPLOADS_DIR = os.path.join(STATIC_DIR, "uploads")
