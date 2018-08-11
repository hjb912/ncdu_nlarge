# -*- coding: UTF-8 -*-
import os
import time
import json
import gzip
import heapq
import logging
import functools

from operator import itemgetter
from args import parser
from logger import init_logger

EXPORT_FILE = 'export.gz'
LOG = logging.getLogger('ncdu')


def extract(file, nlarge=10):
    """
    根据检索到的文件提取完成路径
    :param file 文件名称
    :param nlarge 前n截取显示···
    """
    res = ''
    try:
        with gzip.open(file, 'r') as f:
            res = json.load(f)[3]
    except Exception as e:
        LOG.info(e)
        return

    file_list = []
    parent_path = res[0]['name']
    _extract(res[1:], file_list, parent_path)

    ans = heapq.nlargest(nlarge, file_list, key=itemgetter(1))
    LOG.info('the result (asize: KB):')
    LOG.info('>' * 50)
    for el in ans:
        LOG.info(el)


def _extract(res, file_list, parent_path):
    """
    :param res 读取的资源列表
    :param file_list 保存的文件列表
    :param parent_path 父级路径
    """
    for el in res:
        if isinstance(el, list):
            _parent_path = os.path.join(parent_path, el[0]['name'])
            _extract(el[1:], file_list, _parent_path)
        elif el.get('asize'):
            entire_name = os.path.join(parent_path, el['name'])
            asize = int(el['asize'])
            heapq.heappush(file_list, (entire_name, asize))


def run(args):
    """
    调用ncdu
    :param args 命令行参数
    """

    if args.ssh:
        cmd = f'{args.ssh} ncdu -1xo- {args.start_path}| gzip >{EXPORT_FILE}'
    else:
        cmd = f'ncdu -1xo- {args.start_path} | gzip >{EXPORT_FILE}'

    os.system(cmd)


def clean():
    clean_cmd = 'make clean'
    os.system(clean_cmd)


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        used_time = time.time() - start_time
        LOG.info('>' * 50)
        LOG.info(f'used time: {used_time}')
    return wrapper


@timeit
def main():
    init_logger(logging.INFO)

    args = parser.parse_args()
    run(args)

    extract(EXPORT_FILE, int(args.nlarge))

    clean()


if __name__ == '__main__':
    main()
