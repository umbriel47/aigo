#!/usr/bin/env python
# coding: utf-8

from datetime import datetime

def save_state(db, state, game_id):
    """save current state to database
    """
    timestamp = datetime.utcnow()
    # if state exists update, if not, create a new one