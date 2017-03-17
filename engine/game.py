#!/usr/bin/env python
# encoding: utf-8

from strategies import *
from strategies import utils


COORD = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']

def update(moves, move):
    if moves == '':
        moves = move
    else:
        moves = moves + ',' + move
    return moves

def get_strategy(strategy):
    return utils.get_strategy(strategy)()

def validate(moves, move):
    if move in moves:
        return False
    else:
        return True

def num2coord(move):
    return '%s%s' % (COORD[move[0]], COORD[move[1]])

def get_move(moves, strategy, max_trial=100):
    strategy = utils.get_strategy(strategy)()
    next_move = strategy.get_move(moves)
    trials = 0
    while (not validate(moves, num2coord(next_move))) and trials < max_trial:
            next_move = strategy.get_move(moves)
            trials += 1
    if trials >= max_trial:
        return None
    return num2coord(next_move)


# class Game(object):
#     def __init__(self, moves='', strategy=0):
#         self.coord = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']
#         self.strategy = utils.get_strategy(strategy)()
#         self.MAX_TRIAL = 100
#         self.moves = moves

#     def update(self, move):
#         if self.moves == '':
#             self.moves += move
#         else:
#             self.moves = self.moves + ',' + move

#     def get_move(self, state):
#         """factory function to generate the next next_move
#         """
#         next_move = self.strategy.get_move(state)
#         trials = 0
#         while (not self._validate(state, self._num2coord(next_move))) and trials < self.MAX_TRIAL:
#             next_move = self.strategy.get_move(state)
#             trials += 1
#         return self._num2coord(next_move)

#     def _num2coord(self, move):
#         return '%s%s' % (self.coord[move[0]], self.coord[move[1]])

#     def _validate(self, state, move):
#         if move in state:
#             return False
#         else:
#             return True
        
    

