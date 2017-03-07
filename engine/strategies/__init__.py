#!/usr/bin/env python
# coding: utf-8

strategies = {'rand': 'Random'}

for package, class_name in strategies.items():
    importstring = 'from %s import %s' % (package, class_name)
    exec importstring

