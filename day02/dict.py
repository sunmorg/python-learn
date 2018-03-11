# -*- coding:utf-8 -*-
# Author：sunmorg

info = {
    'sunm': ["ren",18,'web'],
    'zennu':['shen',16,'java']
}

info['woqu'] = ['com',63,'saasd']

print(info.get('sunm')) # get获取
info.pop('sunm') # pop删除 不传参数 随机删
del info['woqu'] # 也可以删除
print(info)