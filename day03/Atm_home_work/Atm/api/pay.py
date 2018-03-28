#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/1/24 20:28.
 * @author: Chinge_Yang.
'''

import os
import sys


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from core import main

if len(sys.argv) < 1:
    exit("\033[31;1mparameters error\033[0m")

amount = int(sys.argv[1])    # 参数1，付款金额
res = main.pay(amount)
if res:
    exit(0)
else:
    exit(1)
