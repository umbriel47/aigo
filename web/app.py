#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from flask import Flask, request, url_for
from flask import render_template, redirect
from flask import session
from flask import flash
from flask_bootstrap import Bootstrap
import pymongo
import datetime
import hashlib
from settings import settings

path = os.path.abspath(__file__)
sys.path.append(path)

print path
from aigo.engine.game import Game

app = Flask(__name__)
app.secret_key = 'aigoisafunnygamehahahahaha'

bootstrap = Bootstrap(app)

db = pymongo.MongoClient('mongodb://%s:%s@%s:%s' % (settings['MONGO_USERNAME'], 
                                                    settings['MONGO_PASSWORD'],
                                                    settings['MONGO_HOST'],
                                                    settings['MONGO_PORT'])).aigo

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<userid>', methods=['GET'])
def user(userid):
    return render_template('user.html', userid=userid)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """user sign in
    """
    if request.method == 'GET':
        return render_template('signin.html')
    if request.method == 'POST':
        email = request.form.get('email')
        password = hashlib.md5(request.form.get('pwd')).hexdigest()
        users = db.users.find(dict(email=email))
        for user in users:
            if password == user['pwd']:
                return redirect(url_for('user', userid=user['_id']))
        flash("User doesn't exist or wrong password")
        return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """user sign up
    """
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        email = request.form.get('email')
        print email
        print db.users.find_one(dict(email=email))
        if db.users.find_one(dict(email=email)) is None:
            password = hashlib.md5(request.form.get('pwd')).hexdigest()
            current = datetime.datetime.utcnow()
            try:
                db.users.save(dict(email=email,
                               pwd=password,
                               timestamp=current
                              )
                         )
                print "user sign up succeed"
            except Exception, e:
                print 'Error creating user: %s' % e
                flash("Error in registering")
                return render_template(url_for('signup'))
            userid_in = db.users.find_one({"email": email})['_id']
            print "get userid"
            return redirect(url_for('user', userid=userid_in))
        else:
            flash("You have registered, please sign-in")
            return redirect(url_for('signin'))


@app.route('/restart', methods=['POST'])
def restart():
    """restart the game
    """
    if 'moves' in session.keys():
        session['moves'] = ''
    return redirect(url_for('index'))

@app.route('/game', methods=['POST'])
def game(id='default'):
    return render_template('game.html', moves='QQ')


# @app.route('/getmove', method=['POST'])
# def getmove():
#     move = request.form.get('move')
#     strategy = request.form.get('strategy')
#     if session['moves'] == '':
#         session['moves'] = move
#         session['strategy'] = strategy
#     else:
#         session['moves'] = session['moves'] + ',' + move
#     # get the AI move
#     ai_move = Game(session['strategy']).get_move(session['moves'])
#     session['moves'] = session['moves'] + ',' + ai_move

#     return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)


