# -*- coding:utf-8 -*-
# Author：sunmorg

names = ["one","two","three"]

def change_name():

    #names = ["three", "two", "one"]
    del names[2]
    # 通过global 来修改全局变量  global需要写在改变之前
    print(names,'里面')
#函数内不能修改整个列表  但是可以修改列表内部的某个元素  或用global来修改整个列表


change_name()
print(names, '外面')