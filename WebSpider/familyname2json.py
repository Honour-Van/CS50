#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file:familyname2json.py
@author: Honour-Van: fhn037@126.com
@date:2021/04/28 00:17:09
@description: transfer the 100 family names txt to json, and then could be easily changed to dict
@version:1.0
'''

import json
d1 = {}
with open("./assets/family_name.txt", 'r', encoding='utf-8') as f:
    for line in f.readlines():
        list1 = line.split()
        for item in list1:
            d1[item[-1]] = 0
with open("assets/family_name.json", 'w', encoding='utf-8') as f:
    json.dump(d1, f)
