#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

def main():
    # 从标准输入读取数据
    for line in sys.stdin:
        # Date,Open,High,Low,Close,Adj Close,Volume
        row=line.split(",")

        # 开盘价
        open_price=float(row[1])
        # 收盘价
        close_price=float(row[-3])

        # 计算价格变化百分比
        price_change=((open_price - close_price)/ open_price )*100

        cheng_text=str(round(price_change, 2))+"%"
        print('{0}\t{1}'.format(cheng_text, 1))
        
if __name__ == '__main__':
    main()