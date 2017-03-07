#!/usr/bin/env python
# coding: utf-8

import random

class Random(object):
    def __init__(self):
        pass

    def get_move(self, state):
        print random
        next_move = (random.randint(0, 18), random.randint(0, 18))
        return next_move