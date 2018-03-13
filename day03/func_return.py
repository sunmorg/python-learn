# -*- coding:utf-8 -*-
# Author：sunmorg

def stu_register(name,age,course='python',country='CN'):

    print("姓名:",name,"年龄：",age,course,country)

    # if age > 22:
    #     return False
    # else:
    #     return True
    return name,age # 得到的是('张三', 16)  元组


stu_status = stu_register("张三",16)
print(stu_status)