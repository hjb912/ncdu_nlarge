# -*- coding: UTF-8 -*-
import os
import time
import json
import gzip
import heapq
import logging

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
        LOG.debug(e)
        return

    file_list = []
    parent_path = res[0]['name']
    _extract(res[1:], file_list, parent_path)

    ans = heapq.nlargest(nlarge, file_list, key=itemgetter('asize'))
    LOG.debug('>' * 50)
    LOG.debug('the resut:\n')
    for el in ans:
        LOG.debug(el)


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
            el['name'] = os.path.join(parent_path, el['name'])
            heapq.heappush(file_list, el)


def run(args):
    """
    调用ncdu
    :param args 命令行参数
    """
    cmd = 'ncdu -1xo- {start_path} | gzip >{export_file}'.format(
        start_path=args.start_path,
        export_file=EXPORT_FILE,
    )
    os.system(cmd)


if __name__ == '__main__':
    init_logger(logging.DEBUG)

    start_time = time.time()
    args = parser.parse_args()
    run(args)
    # 解析中间文件
    extract(EXPORT_FILE, int(args.nlarge))
    LOG.debug('>' * 50)
    LOG.debug('used time:{}'.format(time.time() - start_time))
