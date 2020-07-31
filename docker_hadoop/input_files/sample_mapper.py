#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

for line in sys.stdin:
    line = line.strip()
    row = line.split(',')
    user_id = row[0]
    if user_id == "user_id":
        continue
    birth_year = row[1][0:4]
    gender = row[2]
    print("{0}\t{1}".format(birth_year,gender))