#!_*_coding:utf-8_*_
# __author__:"Alex Li"

'''
handle all the logging works
'''

import logging
import datetime
from conf import settings
from core import bill_date


def logger(log_type):
    # create logger
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL)

    # create file handler and set level to warning
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


def show_log(account, log_type, year_month):
    """
    显示日志内容
    :param user_name: 用户名
    :param log_type: 日志类型
    :return:
    """
    begin_time, end_time = bill_date.get_bill_time(year_month)
    log_file = "%s/log/%s" % (settings.BASE_DIR, settings.LOG_TYPES[log_type])
    file = open(log_file)
    print("-".center(50, "-"))
    for line in file:
        log_time = datetime.datetime.strptime(line.split(",")[0], "%Y-%m-%d %H:%M:%S")
        user_name = line.split()[7].split(":")[1]
        # 帐单生成日是25号，则每月帐单是从上月25日到本月24日之间
        if account == user_name and begin_time <= log_time < end_time:
            print(line.strip())
    print("-".center(50, "-"))
    file.close()
