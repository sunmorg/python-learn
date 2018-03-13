# -*- coding:utf-8 -*-
# Author：sunmorg

#函数内声明的变量为 局部变量


#以下的两个name不是同一个变量  外部即使有 内部也会重新定义
# name = 'sunm'
#
# def change_name():
#     name = '阳光男孩'
#     print(name,'里面改过以后的')
#
#
# change_name()
# print(name,'外面')



#  局部未定义  就访问到全局变量
name = 'sunm'

def change_name():
    print(name,'里面')


change_name()
print(name,'外面')