#!/usr/bin/env python
# encoding: utf-8

from strategies import *
from strategies import utils

class Game(object):
    def __init__(self, strategy=0):
        self.coord = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
        self.strategy = utils.get_strategy(strategy)()
        self.MAX_TRIAL = 100

    def get_move(self, state):
        """factory function to generate the next next_move
        """
        next_move = self.strategy.get_move(state)
        trials = 0
        while (not self._validate(state, self._num2coord(next_move))) and trials < self.MAX_TRIAL:
            next_move = self.strategy.get_move(state)
            trials += 1
        return self._num2coord(next_move)

    def _num2coord(self, move):
        return '%s%s' % (self.coord[move[0]], self.coord[move[1]])

    def _validate(self, state, move):
        if move in state:
            return False
        else:
            return True
        
    

