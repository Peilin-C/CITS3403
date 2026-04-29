import os

basedir = os.path.abspath(os.path.dirname(__file__))
database_location = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    SQLALCHEMY_DATABASE_URI = database_location
    SECRET_KEY = "BestBuddies"

    