import os

SOURCES_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SOURCES_DIR, os.pardir))
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
HTML_TEMPLATE_PATH = os.path.join(RESOURCES_DIR, "index_template.html")
HTML_DESTINATION_PATH = os.path.join(RESOURCES_DIR, "index.html")
