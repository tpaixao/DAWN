from DAWN_framework import DAWN, DB
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import json

app = Flask(__name__)

# Load config ( and override config from an environment variable
global config

try:
    with open('config.json') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    config = {'username': '','postingKey': '', 'db_name': '', 'steem_node': '','first_block': ''}
    with open('config.json','w') as config_file:
        json.dump(config,config_file)
    raise FileNotFoundError("Could not read config.json. Please populate it with relevant details." )
    

try:
    username = config['username']
    postingKey = config['postingKey']
    db_name = config['db_name']
    steem_node = config['steem_node']
    first_block = config['first_block']
except KeyError as er:
    raise KeyError('Could not read required key from config.json.')

# dawn = DAWN()
db = DB('test.db')

#routes

@app.route('/')
def test():
    # return "HELLO"
    # return db.listAssets('tiagouser')
    return db.listAssetHistory('tiagotest/this-is-my-asset')


# API - returns JSON 
# list assets from user
@app.route('/api/user/<string:user>')
def get_user_assets(user):
    return db.listUserOwned(user)
# list history of asset
@app.route('/api/asset/<string:user>/<string:asset>')
def get_asset_history(user,asset):
    return db.listAssetHistory(user + '/' + asset)



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
