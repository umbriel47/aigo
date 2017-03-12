#!/usr/bin/env python
# coding: utf-8

from flask_login import UserMixin

class UserManage(UserMixin):
    is_active = True
    is_anonymous = False
    is_authenticated = True

    def __init__(self, id, email, password):
        self.id = str(id)
        self.email = email
        self.password_hash = password

    def get_id(self):
        return self.id

    def __repr__(self):
        return self.email