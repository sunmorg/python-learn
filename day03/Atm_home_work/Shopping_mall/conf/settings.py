#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2016/12/29 14:52.
 * @author: Chinge_Yang.
'''

import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = {
    'engine': 'file_storage',
    'name': 'accounts',
    'path': "%s/db" % BASE_DIR
}

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'shopping': 'shopping.log',
    'access': 'access.log',
}

