#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2016/12/29 16:31.
 * @author: Chinge_Yang.
'''

import logging
from conf import settings


def logger(log_type, *user_name):
    # create logger
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL)
    # create file handler and set level to warning
    if user_name:
        log_file = "%s/log/%s_%s" % (settings.BASE_DIR, user_name[0], settings.LOG_TYPES[log_type])
    else:
        log_file = "%s/log/%s" % (settings.BASE_DIR, settings.LOG_TYPES[log_type])

    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
    # 'application' code
    '''logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')'''



def show_log(user_name, log_type):
    """
    显示日志内容
    :param user_name: 用户名
    :param log_type: 日志类型
    :return:
    """
    log_file = "%s/log/%s_%s" % (settings.BASE_DIR, user_name, settings.LOG_TYPES[log_type])

    print("User \033[32;1m%s\033[0m shopping history:" % user_name)
    # print("%-20s %-15s %10s %20s" % ("datetime", "Username", "Number", "Goods"))
    file = open(log_file)
    print("-".center(50, "-"))
    for line in file:
        print(line.strip())
    file.close()