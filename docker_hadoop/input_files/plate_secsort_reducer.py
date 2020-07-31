#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

def main():
    # 几乎什么都不用做
    for line in sys.stdin:
        line = line.strip()
        print(line)

if __name__ == '__main__':
    main()