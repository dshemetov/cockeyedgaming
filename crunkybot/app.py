'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''
from __future__ import print_function

from threading import Lock
import json
import logging
import time
import requests
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_oauthlib.client import OAuth
from flask_socketio import SocketIO, emit
from celery import Celery
import eventlet
import config_crunky
#from application import db


eventlet.monkey_patch()

# Flask application initialization.
app = Flask(__name__)
app.config.from_pyfile("config.py")
file_handler = logging.FileHandler(filename='crunkyerr.log')
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

# SocketIO + Celery config.
socketio = SocketIO(app, async_mode="eventlet", message_queue=app.config["SOCKETIO_REDIS_URL"])
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

# Twitch authorization.
oauth = OAuth()
twitch = oauth.remote_app('twitch',
                  base_url='https://api.twitch.tv/kraken/',
                  request_token_url=None,
                  access_token_method='POST',
                  access_token_url='https://api.twitch.tv/kraken/oauth2/token',
                  authorize_url='https://api.twitch.tv/kraken/oauth2/authorize',
                  consumer_key=config_crunky.TWITCH_CLIENTID, # get at: https://www.twitch.tv/kraken/oauth2/clients/new
                  consumer_secret=config_crunky.TWITCH_SECRET,
                  request_token_params={'scope': ["user_read", "channel_check_subscription"]}
                  )

# A general background task to hit a url?
@celery.task()
def background_task(url):
    local_socketio=SocketIO(message_queue=url)
    local_socketio.emit('my_response', {'data': 'Background test starting...'}, namespace="\test")
    time.sleep(10)
    local_socketio.emit('my_response', {'data': 'Background test complete...'}, namespace="\test")

# Starting the background task.
@app.route("/bg")
def start_background_thread():
    background_task.delay(app.config['SOCKETIO_REDIS_URL'])
    return 'Started'

# Unsure.
@socketio.on("my event", namespace="/test")
def test_message(message):
    emit("my response", {"data": 'Backend saw"' + message['data'] + '" from the front end'})

# Standard index2 handler.
@app.route("/index2")
def index2():
    return render_template("index2.html")

# Standard root and index handlers.
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    data={}
    if 'twitch_token' in session:
        headers = {'Authorization': ("OAuth " + session['twitch_token'][0])}
        r = requests.get(twitch.base_url, headers=headers)
        r2 = requests.get(twitch.base_url+"user",headers=headers)
        resp = r2.json()
    if 'status' not in resp:
        data['logo']=resp['logo']
        data['display_name']=resp['display_name']
    elif resp['status'] == 400:
        return redirect(url_for('login'))
    else:
        return "Access denied: Error "+`resp['status']`+", "+resp['message']
    return render_template("index.html",data=data)
    #return "Hello World."

# Something about Twitch API.
@twitch.tokengetter
def get_twitch_token(token=None):
    return session.get('twitch_token')

# Twitch login handler.
@app.route('/login')
def login():
    return twitch.authorize(callback=url_for('authorized', _external=True))

# Twitch authorization output response handler.
@app.route('/login/authorized')
def authorized():
    resp = twitch.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    session['twitch_token'] = (resp['access_token'], '')
    return redirect(url_for('index', _external=True))

# Twitch logout handler.
@app.route('/logout')
def logout():
    session.pop('twitch_token', None)
    return redirect(url_for('index', _external=True))

#if __name__ == '__main__':
#    socketio.run(app,host="http://127.0.0.1:80",debug = True)
