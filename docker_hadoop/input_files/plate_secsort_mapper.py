#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

def main():
    for line in sys.stdin:
        line = line.strip()
        row = line.split(",")
        if len(row) >= 3:
            plate  = row[0]   # 车牌号
            province = row[1] # 注册地
            order = row[2]    # 序号
            mile = row[3]     # 里程
            print(",".join([province, plate, order, mile]))
            
if __name__ == '__main__':
    main()