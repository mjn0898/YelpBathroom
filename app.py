from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('firebase/yelpbathroom-firebase-adminsdk-6s9i6-cab4574a75.json')
default_app = firebase_admin.initialize_app(cred)

app = Flask(__name__)

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

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
