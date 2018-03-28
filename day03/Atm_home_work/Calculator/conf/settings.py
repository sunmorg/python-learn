#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/2/4 14:23.
 * @author: Chinge_Yang.
'''

import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'history': 'history.log'
}