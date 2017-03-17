#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from flask import Flask, request, url_for
from flask import render_template, redirect
from flask import session
from flask import flash, g
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
from flask_bootstrap import Bootstrap
import pymongo
from bson import ObjectId
import datetime
import hashlib
from settings import settings

path = os.path.abspath(__file__)
sys.path.append(path)

# from aigo.engine.game import Game
from aigo.engine import game
from models import UserManage


app = Flask(__name__)
app.secret_key = 'aigoisafunnygamehahahahaha'

bootstrap = Bootstrap(app)

db = pymongo.MongoClient('mongodb://%s:%s@%s:%s' % (settings['MONGO_USERNAME'], 
                                                    settings['MONGO_PASSWORD'],
                                                    settings['MONGO_HOST'],
                                                    settings['MONGO_PORT'])).aigo

# user login management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader  
def load_user(userid):  
    user = db.users.find_one(dict(_id=ObjectId(userid)))
    return UserManage(id=user.get('_id'), email=user.get('email'),
                password=user.get('pwd'))
 
@app.before_request  
def before_request():  
    g.user = current_user  


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/', methods=['GET'])
@login_required
def user():
    games_lst = []
    games = db.games.find(dict(email=current_user.email))
    for game in games:
        game_lst = [game['timestamp'], game['strategy'], game['gamename']]
        games_lst.append(game_lst)
    print games_lst
    return render_template('user.html', games=games_lst)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """user sign in
    """
    if request.method == 'GET':
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = hashlib.md5(request.form.get('pwd')).hexdigest()
        users = db.users.find(dict(email=email))
        for user in users:
            if password == user['pwd']:
                login_user(load_user(user['_id']))
                print current_user
                return redirect(url_for('user'))
        flash("User doesn't exist or wrong password")
        return redirect(url_for('index'))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    print 'You have logged out'
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """user sign up
    """
    if request.method == 'GET':
        return redirect(url_for('index'))
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
            return redirect(url_for('user'))
        else:
            flash("You have already registered, please sign-in")
            return redirect(url_for('index'))


@app.route('/game', methods=['GET', 'POST'])
@login_required
def game_view():
    if ('moves' not in session.keys()) or (session['moves'] is None):
        return redirect(url_for('user'))
    else:
        moves = session['moves']
        strategy = session['strategy']
        return render_template('game.html', moves=moves, strategy=strategy)

@app.route('/getmove', methods=['POST'])
@login_required
def getmove():
    if 'moves' not in session.keys() or session['moves'] is None or session['strategy'] is None:
        return redirect(url_for('user'))
    else:
        new_move = request.form.get('move')
        print session['moves'], new_move
        session['moves'] = game.update(session['moves'], new_move)
        print session['moves']
        ai_move = game.get_move(session['moves'], session['strategy'])
        session['moves'] = game.update(session['moves'], ai_move)
        print session['moves'], ai_move
        return redirect(url_for('game_view'))

@app.route('/creategame', methods=['POST'])
def creategame():
    session['strategy'] = request.form.get('strategy')
    session['moves'] = ''
    session['gamename'] = current_user.email + '+' + str(datetime.datetime.utcnow())
    return redirect(url_for('game_view'))

@app.route('/save', methods=['POST'])
@login_required
def save():
    """save current game
    """
    timestamp = datetime.datetime.utcnow()
    game = db.games.find_one(dict(gamename=session['gamename']))
    if game is not None:
        gameid = game['_id']

        try:
            db.games.save(dict(_id=gameid,
                            moves=session['moves'],
                            gamename=session['gamename'],
                            strategy=session['strategy'],
                            email=current_user.email,
                            timestamp=timestamp
                            )
                        )
        except Exception, e:
            print 'error saving games: %s' % e
            flash('error saving the game')
    else:
        try:
            db.games.save(dict(gamename=session['gamename'],
                        moves=session['moves'],
                        email=current_user.email,
                        strategy=session['strategy'],
                        timestamp=timestamp
                        )
                    )
        except Exception, e:
            print 'error saving games: %s' % e
            flash('error saving the game')
    
    flash('game saved')
    return redirect(url_for('game_view'))    


@app.route('/load_game/<gamename>', methods=['GET'])
@login_required
def load_game(gamename):
    """get the specific game
    """
    print gamename
    game = db.games.find_one(dict(gamename=gamename))
    if game is None:
        print 'Error loading the game'
        flash('Error loading the game')
        return redirect(url_for('user'))
    else:
        session['strategy'] = game['strategy']
        session['moves'] = game['moves']
        session['gamename'] = game['gamename']
    return redirect(url_for('game_view'))


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


