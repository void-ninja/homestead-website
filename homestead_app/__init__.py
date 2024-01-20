import os
from datetime import datetime
import pytz
import re

from flask import Flask, render_template, redirect, request, url_for, flash
from . import db
from .date_format import *

TIMEZONE = 'America/Detroit'

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'fcf05b1e0cdc6c6b97d5aea8ac229c54672aa9684db5a9c11571a49da63d'
app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'homestead.sqlite'),
)

# ensure the instance folder exists 
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


@app.route('/')
def index():
    return redirect(url_for('chickens'))    

#! IMPORTANT: When getting the dates from the website, format them to
#! YYYY/MM/DD with the format_date_year_first function, as this is how
#! they are stored in the SQLite database, to allow for sorting by date
#! accurately. When sending them to the website, format them back by using
#! format_date_month_first

@app.route('/chickens', methods=('GET', 'POST'))
def chickens():
    eggs = ''
    notes =''
        
    zone = pytz.timezone(TIMEZONE)
    date = datetime.now(zone).strftime('%Y/%m/%d')#YYYY/MM/DD
    time = datetime.now(zone).strftime('%I:%M')
    
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
    
    return render_template('chickens.html', is_today=True, date=format_date_month_first(date), time=time, todays_eggs=eggs, notes=notes)

@app.route('/chickens/old/<target_date>', methods=('GET', 'POST'))
def chickens_old(target_date):
    eggs =''
    notes =''
    date = format_date_year_first(re.sub('S', '/', target_date))
    
    conn = db.get_db()
    days_eggs = conn.execute('SELECT * FROM eggs WHERE collection_date = :date',{'date': date}).fetchone()
    
    if days_eggs:
        eggs = days_eggs[1] #get egg count
        if days_eggs[2]:
            notes = days_eggs[2] #get note
            
    
    if request.method == 'POST':
        date = format_date_year_first(request.form.get('form_date'))
        
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
    
    return render_template('chickens.html', is_today=False, date=format_date_month_first(date), todays_eggs=eggs, notes=notes)

@app.route('/chickens/egg_log', methods=('GET', 'POST'))
def egg_log():
    conn = db.get_db()
    
    if request.method == 'POST':
        match request.form.get('form_id'):
            case 'add_entry':
                new_date = format_date_year_first(request.form.get('date_input'))
                if conn.execute('SELECT * FROM eggs WHERE collection_date = :date',{'date': new_date}).fetchone() :
                    flash('An entry with that date already exists!')
                elif new_date == '' or new_date == '2024/00/00':
                    flash('Please enter a date')
                elif not re.search(r'^\d\d\/\d\d\/\d\d\d\d$', format_date_month_first(new_date)):
                    flash('Please enter a date that matches the form MM/DD/YYYY')
                else:
                    conn.execute('INSERT INTO eggs (collection_date, amount) VALUES (:date, 0)',{'date': new_date})
                    conn.commit()
                return redirect(url_for('egg_log'))
                    
            case 'edit':
                date = request.form.get('date')
                date = re.sub('/', 'S', date)
                return redirect(url_for('chickens_old', target_date=date))
            case 'delete':
                date = format_date_year_first(request.form.get('date')) 
                conn.execute('DELETE FROM eggs WHERE collection_date = :date',{'date': date})
                conn.commit()
                return redirect(url_for('egg_log'))
                
    
    logs = conn.execute('SELECT * FROM eggs ORDER BY collection_date').fetchall()
    conn.close()
    logs = list(reversed(logs))
    
    eggs = []
    
    for log in logs:
        temp = []
        for i in log:
            temp.append(i)
            
        temp[0] = format_date_month_first(temp[0])
        
        eggs.append(temp)
        
        
    return render_template('egg_log.html', eggs=eggs)

@app.route('/rabbits')
def rabbits():
    zone = pytz.timezone(TIMEZONE)
    date = datetime.now(zone).strftime('%m/%d/%Y')#MM/DD/YYYY
    time = datetime.now(zone).strftime('%I:%M')
    return render_template('rabbits.html', is_today=True, date=date, time=time)

@app.route('/garden')
def garden():
    zone = pytz.timezone(TIMEZONE)
    date = datetime.now(zone).strftime('%m/%d/%Y')#MM/DD/YYYY
    time = datetime.now(zone).strftime('%I:%M')
    return render_template('garden.html', is_today=True, date=date, time=time)

db.init_app(app)