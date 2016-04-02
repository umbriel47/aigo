#-*-coding:utf-8-*-
#

import player
from strategy import *

class Computer(player.Player):
    def __init__(self, symbol, method):
        self.symbol = symbol
        self.method = method

    def generate_move(self, board):
        loc_x, loc_y = eval(self.method)(board)
        return (loc_x, loc_y)
