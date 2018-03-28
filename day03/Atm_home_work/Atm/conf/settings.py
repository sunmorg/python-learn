#!_*_coding:utf-8_*_
# __author__:"Alex Li"
import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BILL_DAY = 25

DATABASE = {
    'engine': 'file_storage',  # support mysql,postgresql in the future
    'name': 'accounts',
    'path': "%s/db" % BASE_DIR
}

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log',
}

LOG_DATABASE = {
    'engine': 'file_storage',  # support mysql,postgresql in the future
    'name': 'accounts',
    'path': "%s/log" % BASE_DIR
}

TRANSACTION_TYPE = {
    'repay': {'action': 'plus', 'interest': 0}, # 还款
    'receive': {'action': 'plus', 'interest': 0},   # 接收
    'withdraw': {'action': 'minus', 'interest': 0.05},  # 提款
    'transfer': {'action': 'minus', 'interest': 0.05},  # 转出
    'pay': {'action': 'minus', 'interest': 0},  # 支付
    'save': {'action': 'plus', 'interest': 0},  # 存钱

}

ACCOUNT_FORMAT = {
    """
    用户数据库格式
    {"enroll_date": "2016-01-02", "password": "abc", "id": 1000, "credit": 15000,
     "status": 0, "balance": 1000.0, "expire_date": "2021-01-01", "pay_day": 22}
    """
}