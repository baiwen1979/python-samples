#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

num_by_gender = {'0': 0, '1': 0, '2': 0}
last_key = False
for line in sys.stdin:
    line = line.strip()    
    row = line.split('\t')
    cur_key = row[0]
    gender = row[1]
    if last_key and cur_key != last_key:
        print("Y:{0},F:{1},M:{2}".
              format(last_key,num_by_gender['0'],num_by_gender['1']))
        last_key = cur_key
        num_by_gender = {'0': 0, '1': 0, '2': 0}
        num_by_gender[gender] += 1
    else:
        last_key = cur_key
        num_by_gender[gender] += 1
        
if last_key:
    print("Y:{0},F:{1},M:{2}".
          format(last_key,num_by_gender['0'],num_by_gender['1']))