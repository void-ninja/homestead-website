import os
from datetime import datetime
import pytz

from flask import Flask, render_template, redirect

TIMEZONE = "America/Detroit"

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route("/")
    def index():
        return redirect(Flask.url_for(app,"chickens"))    
    
    @app.route('/chickens')
    def chickens():
        zone = pytz.timezone(TIMEZONE)
        date = datetime.now(zone).strftime("%x") #MM/DD/YYYY
        hour = datetime.now(zone).strftime("%I") #HH
        minute = datetime.now(zone).strftime("%M") #mm
        time = hour + ":" + minute
        return render_template("chickens.html", date=date, time=time)
    
    @app.route("/rabbits")
    def rabbits():
        zone = pytz.timezone(TIMEZONE)
        date = datetime.now(zone).strftime("%x") #MM/DD/YYYY
        hour = datetime.now(zone).strftime("%I") #HH
        minute = datetime.now(zone).strftime("%M") #mm
        time = hour + ":" + minute
        return render_template("rabbits.html", date=date, time=time)
    
    @app.route("/garden")
    def garden():
        zone = pytz.timezone(TIMEZONE)
        date = datetime.now(zone).strftime("%x") #MM/DD/YYYY
        hour = datetime.now(zone).strftime("%I") #HH
        minute = datetime.now(zone).strftime("%M") #mm
        time = hour + ":" + minute
        return render_template("garden.html", date=date, time=time)

    from . import db
    db.init_app(app)
    
    return app