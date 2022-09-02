from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import os

def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")



app = Flask("__main__")
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLPATH")
db = SQLAlchemy(app)


def create_app():
    # sched = BackgroundScheduler(daemon=True)
    # sched.add_job(sensor,'interval',seconds=6)
    # sched.start()
    # db.create_all()
    return app