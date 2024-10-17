from .config import Config


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/prod_todo_db"
