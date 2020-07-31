#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

def main():
    for line in sys.stdin:
        line = line.strip()
        seq = line.split(",")
        if len(seq) >= 3:
            plate  = seq[0] #车牌号
            province = seq[1] #注册地
            mile = seq[2] #里程
            print(province + "," + plate + "\t" + mile) 

if __name__ == '__main__':
    main()