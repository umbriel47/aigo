#-*-coding:utf-8-*-
#

import os
import copy
import numpy as np

class Board(object):
    def __init__(self, size=19):
        total_size = size*size
        self.board_mark = u'\u253c'
        board = [self.board_mark]*total_size
        lst = 'abcdefghijklmnopqrstuvwxyz'
        self.col_label = ' \t'
        for idx in range(size):
            self.col_label += '%s ' % lst[idx]
        self.size = size
        self.board = np.reshape(board, (size, size))
        self.cluster = []
        self.remove = []
        self.pre_remove = []
        self.pre_locate = None

    def update(self, loc_x, loc_y, val):
        if loc_x < 0 or loc_x >= self.size or loc_y < 0 or loc_y >= self.size:
            print 'Error: location out of range'
            return False
        current_val = self.board[loc_x, loc_y]
        if self.valid_move(loc_x, loc_y, val):
            for x, y in self.remove:
                self.board[x, y] = self.board_mark
            self.pre_remove = self.remove
            self.pre_locate = (loc_x, loc_y)
            self.remove = []
            return True
        else:
            self.board[loc_x, loc_y] = current_val
            return False

    def get_board(self):
        return self.board

    def get_ptStatus(self, loc_x, loc_y):
        if loc_x < 0 or loc_x >= self.size or loc_y < 0 or loc_y >= self.size:
            print 'Error: get_ptStatus: location out of range'
            return None
        return self.board[loc_x, loc_y]

    def valid_move(self, loc_x, loc_y, val):
        """
        check if current configuration is legal
        """
        if self.board[loc_x, loc_y] != self.board_mark:
            return False
        self.board[loc_x, loc_y] = val        
        remove = []
        neighbors = self.get_neighbor(loc_x, loc_y)
        for x, y in neighbors:
            pt_val = self.get_ptStatus(x, y)
            if (pt_val != val) and (pt_val != self.board_mark):
                alive, cluster = self.get_cluster(x, y, pt_val)
                if alive == False:
                    remove += cluster
        if len(remove) > 0:
            if len(remove) == 1 and self.pre_locate == remove[0] and len(self.pre_remove) == 1 and self.pre_remove[0] == (loc_x, loc_y):
                return False
            self.remove = remove
            return True
        else:
            alive, cluster = self.get_cluster(loc_x, loc_y, val)
            if alive:
                return True
            else:
                return False
           

    def get_neighbor(self, loc_x, loc_y):
        neighbor = []
        lst = ((loc_x - 1, loc_y), (loc_x + 1, loc_y), (loc_x, loc_y - 1), (loc_x, loc_y + 1))
        for x, y in lst:
            if x < 0 or y < 0 or x >= self.size or y >= self.size:
                continue
            else:
                neighbor.append((x, y))
        return neighbor

    def get_cluster(self, loc_x, loc_y, val):
        if loc_x < 0 or loc_x >= self.size or loc_y < 0 or loc_y >= self.size:
            print 'Error: _get_cluster: location out of range'
            return []
        cluster = []
        cluster.append((loc_x, loc_y))
        neighbor = self.get_neighbor(loc_x, loc_y)
        # return_flag = True # control the loop
        alive_flag = False
        while True:
            neighbor_tmp = neighbor
            neighbor = []
            for x_loc, y_loc in neighbor_tmp:
                pt_val = self.get_ptStatus(x_loc, y_loc)
                if pt_val == self.board_mark:
                    alive_flag = True
                elif (x_loc, y_loc) not in cluster and pt_val == val:
                    cluster.append((x_loc, y_loc))
                    neighbor_1 = self.get_neighbor(x_loc, y_loc)
                    for item in neighbor_1:
                        neighbor.append(item)
            if neighbor == []:
                break
        return alive_flag, cluster

    def clean_board(self):
        """
        remove dead stones from the board
        """
        pass

    def view(self):
        os.system('clear')
        print self.col_label
        rows = 1
        for row in self.board:
            out_str = ''.join([state + '-' for state in row])
            print '%d\t%s' % (rows, out_str)
            rows += 1

