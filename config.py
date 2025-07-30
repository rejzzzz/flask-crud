import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')

    SECRET_KEY = os.getenv('SECRET_KEY')

    JSON_SORT_KEYS = False
    PROPAGATE_EXCEPTIONS = True

class dev(Config):
    DEBUG = True

class prod(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')


config = {
    'development': dev,
    'production': prod,
}