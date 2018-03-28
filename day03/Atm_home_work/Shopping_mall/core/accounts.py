#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2016/12/29 16:31.
 * @author: Chinge_Yang.
'''

import json
import time
from core import db_handler
from conf import settings


def load_account_info(account_id):
    '''
    return account balance and other basic info
    :param account_id:
    :return:
    '''
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account_id)
    with open(account_file) as f:
        acc_data = json.load(f)
        return acc_data


def dump_account(account_data):
    '''
    after updated transaction or account data , dump it back to file db
    :param account_data:
    :return:
    '''
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account_data['user'])
    with open(account_file, 'w') as f:
        acc_data = json.dump(account_data, f)

    return True
