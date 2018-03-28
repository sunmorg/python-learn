#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2016/12/29 14:52.
 * @author: Chinge_Yang.
'''

import os
from core import db_handler
from conf import settings
from core import logger
from core import accounts
import json
import datetime


def acc_auth(account, password):
    global new_user
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account)
    # print(account_file)
    if os.path.isfile(account_file):
        new_user = False  # 标记为老用户
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            if account_data['password'] == password:
                return account_data
            else:
                print("\033[31;1mAccount or password is incorrect!\033[0m")
    else:
        new_user = True  # 标记为新用户
        print("Account [\033[31;1m%s\033[0m] does not exist!" % account)


def acc_login(user_data, log_obj):
    '''
    account login func
    :user_data: user info data , only saves in memory
    :return:
    '''
    retry_count = 0
    same_user_count = 0
    last_user = ""  # 最后一次登录的用户
    while user_data['is_authenticated'] is not True and retry_count < 3:
        print("Please input your user name and password!")
        user = input("\033[32;1muser:\033[0m").strip()
        password = input("\033[32;1mpassword:\033[0m").strip()
        if last_user == user:
            same_user_count += 1
        auth = acc_auth(user, password)
        if auth:  # 有返回
            user_data['is_authenticated'] = True
            user_data['user'] = user
            money = auth["balance"]  # 记录用户余额
            old_money = money  # 旧余额
            return auth

        last_user = user
        retry_count += 1
    else:
        print(same_user_count)
        if same_user_count == retry_count - 1:
            log_obj.error("account [%s] too many login attempts" % user)
        exit()


def sign_up(user_data):
    """
    用户注册
    :param user_data:
    :return:
    """
    exist_flag = True
    while exist_flag is True:
        user = input("\033[32;1muser:\033[0m").strip()
        password = input("\033[32;1mpassword:\033[0m").strip()
        exist_flag = acc_check(user)
        if exist_flag:
            print("Account [\033[31;1m%s\033[0m] is exist,try another account." % user)
            exist_flag = True
            continue
        else:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            account_data = {"enroll_date": today, "balance": 0, "password": password, "user": user, "status": 0}
            accounts.dump_account(account_data)
            user_data['is_authenticated'] = True
            user_data['user'] = user
            user_data['account_data'] = account_data
            return True


def acc_check(account):
    '''
    查找帐号是否存在
    :param account: credit account number
    :return: 帐号存在返回真，否则返回假
    '''
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account)
    if os.path.isfile(account_file):
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            return account_data
