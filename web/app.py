#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from flask import Flask, request, url_for
from flask import render_template, redirect
from flask import session

path = os.path.abspath(__file__)
sys.path.append(path)

print path
from aigo.engine.game import Game

app = Flask(__name__)
app.secret_key = 'aigoisafunnygamehahahahaha'



@app.route('/')
def index():
    if 'moves' not in session.keys():
        session['moves'] = ''
    return render_template('index.html', moves=session['moves'])

@app.route('/game/<id>', methods=['POST'])
def game(id='default'):
    if request.method == 'POST':
        move = request.form.get('move')
        strategy = request.form.get('strategy')
        if session['moves'] == '':
            session['moves'] = move
            session['strategy'] = strategy
        else:
            session['moves'] = session['moves'] + ',' + move
        # get the AI move
        ai_move = Game(session['strategy']).get_move(session['moves'])
        session['moves'] = session['moves'] + ',' + ai_move

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)


