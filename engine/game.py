#!/usr/bin/env python
# encoding: utf-8


import numpy as np
from strategies import *
from utils import *

class Game(object):
    def __init__(self):
        self.state = np.zeros(19, 19)
        self.colors = (-1, 1)  # -1: black, 1: white
        self.current_color = -1

    def start(self):
        print 'start the game'


    def _get_move(self, state, strategy):
        """factory function to generate the next next_move
        """
        next_move = strategy.get(status)

    def _update(status, move):
        x, y = move['coord']
        self.state[x, y] = move['color']
    

