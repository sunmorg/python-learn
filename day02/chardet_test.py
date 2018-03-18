# -*- coding:utf-8 -*-
# Author：sunmorg

import chardet
# 自动检测编码模块
f = open("test.txt","rb")
data = f.read()
print(chardet.detect(data))