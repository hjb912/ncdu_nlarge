# -*- coding: utf-8 -*-
import logging


def init_logger(level):

    logger = logging.getLogger("ncdu")
    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter("[%(levelname)s]: %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)