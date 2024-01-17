import sqlite3
import click
from flask import current_app,g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
        
def init_db():
    db = get_db()
    
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
        
# to run this, type the command flask --app homestead_app init-db
@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    click.echo('WARNING! This will clear the table and reset it, deleting all information stored in it.')
    click.echo('This runs the schema.sql file.')
    click.confirm('Are you sure you want to continue?', abort=True)
    init_db()
    click.echo('Initialized the database.')
    

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)