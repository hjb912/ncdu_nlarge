# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser(description='ndcu')
parser.add_argument('-p', default='.', dest='start_path', help='指定开始检索路径, 默认.')
parser.add_argument('-n', dest='nlarge', default=10, help='指定获取展示大文件数量, 默认10')
parser.add_argument('-ssh', dest='ssh', default='', help='通过ssh获取远端机器信息')


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
