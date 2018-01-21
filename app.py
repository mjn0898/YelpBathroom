from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from flask import g
from time import gmtime, strftime
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , flaskr.py


app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'app.db'),
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='root'
))

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
                        
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')
    
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/create', methods=['POST'])
def create():
    db = get_db()
    db.execute('insert into entries (title, description) values (?, ?)',
               [request.form['title'], request.form['desc']])
    db.commit()
    return redirect(url_for('list'))

@app.route('/remove/<entry_title>/<entry_desc>', methods=['POST'])
def remove(entry_title, entry_desc):
    db = get_db()
    db.execute('delete from entries where title=? and description=? limit 1', [entry_title, entry_desc])
    db.commit()
    flash('Entry ' + entry_title + ' was deleted')
    return redirect(url_for('list'))

@app.route('/list', methods=['GET'])
def list():
    db = get_db()
    cur = db.execute('select title, description from entries order by title asc')
    entries = cur.fetchall()
    return render_template('list.html', entries=entries)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
