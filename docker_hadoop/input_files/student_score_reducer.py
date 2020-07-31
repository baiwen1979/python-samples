#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

def main():
    sname = None
    for line in sys.stdin:
        line = line.strip()
        row = line.split('\t')
        name = row[2]
        if name == '-':
            row[2] = sname
            print('\t'.join([row[0], row[2], row[1], row[3]]))
        else:
            sname = name

if __name__ == '__main__':
    main()