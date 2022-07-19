from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask("__main__")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLPATH")
db = SQLAlchemy(app)


def create_app():
    # db.create_all()
    return app