#!/usr/bin/env python
# coding: utf-8

from aigo.engine.strategies import *

def get_strategy(strategy_name):
    return globals()[strategy_name]