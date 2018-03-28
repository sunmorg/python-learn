# -*- coding:utf-8 -*-
# Author：sunmorg

import logging


logging.basicConfig(filename='log_test.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(lineno)d:%(process)d %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')


logging.debug('is when this event was logged.')
logging.warning('is when this event was logged.')