import os
from datetime import datetime
import pytz
import re


from flask import Flask, render_template, redirect, request, url_for
from . import db

TIMEZONE = 'America/Detroit'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'fcf05b1e0cdc6c6b97d5aea8ac229c54672aa9684db5a9c11571a49da63d'
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'homestead.sqlite'),
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


    @app.route('/')
    def index():
        return redirect(url_for('chickens'))    
    
    @app.route('/chickens', methods=('GET', 'POST'))
    def chickens():
        eggs = ''
        notes =''
            
        zone = pytz.timezone(TIMEZONE)
        date = datetime.now(zone).strftime('%x') #MM/DD/YYYY
        hour = datetime.now(zone).strftime('%I') #HH
        minute = datetime.now(zone).strftime('%M') #mm
        time = hour + ':' + minute
        
        conn = db.get_db()
        todays_eggs = conn.execute('SELECT * FROM eggs WHERE collection_date = :date',{'date': date}).fetchone()
        
        if todays_eggs:
            eggs = todays_eggs[1] #get egg count
            if todays_eggs[2]:
                notes = todays_eggs[2] #get note
                
        
        if request.method == 'POST':
            if request.form.get('form_id') == '1': #log eggs
                amount = request.form['eggs-to-log']
                
                if todays_eggs:
                    amount = int(amount) + eggs
                    conn.execute('UPDATE eggs SET amount = :amount WHERE collection_date = :date',{'amount': amount, 'date': date})
                    conn.commit()
                else:
                    conn.execute('INSERT INTO eggs (collection_date, amount) VALUES (:date, :amount)',{'date': date,'amount': amount})
                    conn.commit()
                return redirect(url_for('chickens'))
            
            elif request.form.get('form_id') == '2': # save note
                new_note = request.form['notes']
                
                if todays_eggs:
                    conn.execute('UPDATE eggs SET notes = :note WHERE collection_date = :date',{'note': new_note, 'date': date})
                    conn.commit()
                else:
                    conn.execute('INSERT INTO eggs (collection_date, amount, notes) VALUES (:date, 0, :note)',{'note': new_note, 'date': date})
                    conn.commit()
                return redirect(url_for('chickens'))
            
        
        conn.close()
        
        return render_template('chickens.html', is_today=True, date=date, time=time, todays_eggs=eggs, notes=notes)
    
    @app.route('/chickens/old/<target_date>', methods=('GET', 'POST'))
    def chickens_old(target_date):
        eggs =''
        notes =''
        date = re.sub('S', '/', target_date)
        
        conn = db.get_db()
        days_eggs = conn.execute('SELECT * FROM eggs WHERE collection_date = :date',{'date': date}).fetchone()
        
        if days_eggs:
            eggs = days_eggs[1] #get egg count
            if days_eggs[2]:
                notes = days_eggs[2] #get note
                
        
        if request.method == 'POST':
            
            date = request.form.get('form_date')
            
            if request.form.get('form_id') == '1': #log eggs
                amount = request.form['eggs-to-log']
                
                if days_eggs:
                    amount = int(amount) + eggs
                    conn.execute('UPDATE eggs SET amount = :amount WHERE collection_date = :date',{'amount': amount, 'date': date})
                    conn.commit()
                else:
                    conn.execute('INSERT INTO eggs (collection_date, amount) VALUES (:date, :amount)',{'date': date,'amount': amount})
                    conn.commit()
                return redirect(url_for('chickens_old', target_date=target_date))
            
            elif request.form.get('form_id') == '2': # save note
                new_note = request.form['notes']
                
                if days_eggs:
                    conn.execute('UPDATE eggs SET notes = :note WHERE collection_date = :date',{'note': new_note, 'date': date})
                    conn.commit()
                else:
                    conn.execute('INSERT INTO eggs (collection_date, amount, notes) VALUES (:date, 0, :note)',{'note': new_note, 'date': date})
                    conn.commit()
                return redirect(url_for('chickens_old', target_date=target_date))
        
        conn.close()
        
        return render_template('chickens.html', is_today=False, date=date, todays_eggs=eggs, notes=notes)
    
    @app.route('/chickens/egg_log', methods=('GET', 'POST'))
    def egg_log():
        if request.method == 'POST':
            date = request.form.get('date')
            date = re.sub('/', 'S', date)
            return redirect(url_for('chickens_old', target_date=date))
            
        
        connection = db.get_db()
        logs = connection.execute('SELECT * FROM eggs').fetchall()
        connection.close()
        logs = list(reversed(logs))
        return render_template('egg_log.html', eggs=logs)
    
    @app.route('/rabbits')
    def rabbits():
        zone = pytz.timezone(TIMEZONE)
        date = datetime.now(zone).strftime('%x') #MM/DD/YYYY
        hour = datetime.now(zone).strftime('%I') #HH
        minute = datetime.now(zone).strftime('%M') #mm
        time = hour + ':' + minute
        return render_template('rabbits.html', date=date, time=time)
    
    @app.route('/garden')
    def garden():
        zone = pytz.timezone(TIMEZONE)
        date = datetime.now(zone).strftime('%x') #MM/DD/YYYY
        hour = datetime.now(zone).strftime('%I') #HH
        minute = datetime.now(zone).strftime('%M') #mm
        time = hour + ':' + minute
        return render_template('garden.html', date=date, time=time)

    db.init_app(app)
    
    return app