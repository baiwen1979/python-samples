#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

def main():
    # 输入来自标准输入STDIN (标准输入)
    for line in sys.stdin:
        # 移除开始和结尾的空白字符
        line = line.strip()
        # 将每行分割为单词
        words = line.split()
        # 计数
        for word in words:
            # 将结果写入到STDOUT (标准输出);
            # 这里的输出将成为Reduce阶段的输入，即reducer.py的输入
            # 单词及其计数使用tab符分隔
            print('{0}\t{1}'.format(word, 1))

if __name__ == '__main__':
    main() 