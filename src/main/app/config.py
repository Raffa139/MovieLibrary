from environment import database_uri


class Config:
    SQLALCHEMY_DATABASE_URI = database_uri()
