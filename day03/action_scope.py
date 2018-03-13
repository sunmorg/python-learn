# -*- coding:utf-8 -*-
# Author：sunmorg

# 在python中  作用域类似于JavaScript中的作用域

# 代码定义完成后，作用域就已经生成，作用域链向上查找

age = 18

def func1():
    age = 23
    print("sunm:",age)
    def func2():
        print("zennu",age)
    return func2

val = func1()
val() # val 指向func1中的func2  代码定义完成后，作用域就已经生成，作用域链向上查找