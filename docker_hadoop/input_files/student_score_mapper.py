#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

def main():
    for line in sys.stdin:
        line = line.strip()
        row = line.split(',')
        sid = row[0]
        if sid == 'sid':
            continue
        if len(row) == 2:
            name = row[1]
            course = '-'
            score = '-'            
        else:
            name = '-'
            course = row[1]
            score = row[2]
        print('\t'.join((sid, course, name, score)))

if __name__ == '__main__':
    main()