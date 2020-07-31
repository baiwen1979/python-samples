#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
def main():
    # 定义变量存储 单词 和 词频
    current_word = None 
    current_count = 1

    for line in sys.stdin:
        # 读取mapper函数输出的结果
        word, count = line.strip().split("\t")

        # 判断当前是否存单词
        if current_word:
            if word == current_word:
                current_count += int(count)
            else:
                print('{0}\t{1}'.format(current_word, current_count))
                current_count = 1
        # 赋值当前单词
        current_word = word

    # 处理最后一行数据
    if current_count >= 1:
        print('{0}\t{1}'.format(current_word, current_count))

if __name__ == '__main__':
    main()