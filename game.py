#-*-coding:utf-8-*-
#

# main class to handle the game

import board
import player

class Game(object):
    def __init__(self, size, players):
        self.size = size
        self.bd = board.Board(size)
        self.players = players
        self.current_player = 0
        lst = 'abcdefghijklmnopqrstuvwxyz'
        self.col = {}
        for idx, val in enumerate(lst):
            if idx < size:
                self.col[val] = idx
            else:
                break

    def start(self):
        while True:
            player = self.players[self.current_player]
            self.bd.view()
            
            if self._get_loc():
                if self.bd.update(self.x, self.y, player.get_symbol()):
                    self.current_player = (self.current_player + 1) % 2

                else:
                    print 'Illegal move'
                    raw_input()

    def _get_loc(self):
        move = raw_input('\nPlayer %d move (e.g., b2): ' % (self.current_player + 1))
        try:
            col = move[0]
            row = move[1:]
            row = int(row)
            col = col.lower()
        except Exception, e:
            print 'illegal move'
            return False
        if col not in self.col.keys() or row < 1 or row > self.size:
            print 'illegal move'
            return False
        self.y = self.col[col]
        self.x = row - 1
        return True

