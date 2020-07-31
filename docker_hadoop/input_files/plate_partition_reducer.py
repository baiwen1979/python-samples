#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

def main():
    prov = None
    sum_mile = 0

    for line in sys.stdin:
        line = line.strip()
        row, mile = line.split("\t")
        mile = int(mile)
        if prov == None:
            prov = row[0].split(",")[0]
            sum_mile = mile
        else:
            if prov == row[0].split(",")[0]:
                # 相同组
                sum_mile += mile
            else:
                # 不同组，输出上一组数据
                print('{0}\t{1}'.format(prov, sum_mile))
                sum_mile = mile
                prov = row[0].split(",")[0]

    print('{0}\t{1}'.format(prov, sum_mile))

if __name__ == '__main__':
    main()