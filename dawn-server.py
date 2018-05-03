from DAWN_framework import DAWN, DB
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('DAWN_SETTINGS', silent=True)

# dawn = DAWN()
db = DB('test.db')


@app.route('/')
def test():
    return "HELLO"

# TODO
@app.route('/login',methods=['GET', 'POST'] )
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('/'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    return redirect( url_for('/') )
