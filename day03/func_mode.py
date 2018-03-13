# -*- coding:utf-8 -*-
# Author：sunmorg

# def stu_register(name,age,counyry,course):
#     print("registriation info....")
#     print(name,age,counyry,course)
#
# stu_register("sunm","18","ch","python")



#默认参数的放在未知参数后
def stu_register(name, age, course, country = "ch"):
    print("registriation info....")
    print(name, age, country, course)

# stu_register("sunm", "18", "python")
# stu_register("sunm", "18", "python","as")



#关键参数得放在未知参数后面，关键参数带上参数命就可不按顺序
stu_register(age="26",country="jp",course="py",name="ssss")


#  报警，起初一个人员
# def send_alert(msg,user):
#     pass


#  报警，现在公有一个团队运维  得一个个调用  所以是不现实的  改进代码


#非固定参数
#参数前加个 字符 *
def send_alert(msg,*user):
    for i in user:
        print(i,"警告")

#调用  第一个是msg参数   后面以元组的方式传给send_alert方法

#如果参数中出现了  *user，被传递的参数就可以不再是固定的个数，传过来的所有参数打包成元组发送到方法内部
#方式一
# send_alert("警告","a","b","c")
#方式二  如果传递的是列表或者元组   在元组 和 列表前加  *
#send_alert("警告",*["a","b","c"])







