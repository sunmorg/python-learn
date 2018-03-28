#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/1/26 20:46.
 * @author: Chinge_Yang.
'''

from conf import settings
import datetime


def get_bill_time(year_month):
    """
    获取给出的年-月的信用卡帐单月份起止时间
    :param year_month: 年-月
    :return: 返回日期
    """
    the_bill_day = "%s-%s" % (year_month, settings.BILL_DAY)  # 帐单日
    bill_begin_time = datetime.datetime.strptime(the_bill_day, "%Y-%m-%d")  # 给出的年-月帐单开始时间
    year = bill_begin_time.year
    month = bill_begin_time.month
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    bill_end_time = datetime.datetime(year, month, settings.BILL_DAY)
    return bill_begin_time, bill_end_time
