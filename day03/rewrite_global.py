# -*- coding:utf-8 -*-
# Author：sunmorg

name = 'sunm'

def change_name():
    global name
    name = '阳光男孩'
    # 通过global 来修改全局变量  global需要写在改变之前
    print(name,'里面改过以后的')

change_name()
print(name, '外面')