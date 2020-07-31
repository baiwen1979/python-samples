#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def main():
    current_word = None
    current_count = 0
    word = None

    # 输入来自STDIN
    for line in sys.stdin:
        # 移除开始和结尾的空白字符
        line = line.strip()

        # 解析来自mapper的单词和频率
        word, count = line.split('\t', 1)

        # 将计数值（字符串）转化为整数
        try:
            count = int(count)
        except ValueError:
            # 如果不是数值，则跳过
            # 忽略/抛弃此行
            continue
        # 下面的计数代码有效是因为Hadoop在将map输出交给reducer之前按键进行了排序
        if current_word == word:
            current_count += count
        else:
            if current_word:
                # 写入到标准输出STDOUT
                print('{0}\t{1}'.format(current_word, current_count))
            current_count = count
            current_word = word
    # 输出最后一个单词及其计数
    if current_word == word:
        print('{0}\t{1}'.format(current_word, current_count))

if __name__ == '__main__':
    main()