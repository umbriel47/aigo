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

@app.route('/game/<id>', methods=['POST', 'GET'])
def game(id='default'):
    if request.method == 'GET':
        return 'game get request %s' % id
    if request.method == 'POST':
        move = request.form.get('move')
        if session['moves'] == '':
            session['moves'] = move
        else:
            session['moves'] = session['moves'] + ',' + move
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)


