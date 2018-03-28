#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2016/12/28 14:36.
 * @author: Chinge_Yang.
'''

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(base_dir)
sys.path.append(base_dir)

from core import main

if __name__ == '__main__':
    main.manage_run()


