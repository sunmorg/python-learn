# -*- coding:utf-8 -*-
# Author：sunmorg

class Student:
    school = '清华大学'

    def __init__(self,name,sex,age):
        self.Name = name
        self.Sex = sex
        self.Age = age

    def learn(self):
        print('is learning')

    def eat(self):
        print('is eating')

    def sleep(self):
        print('is sleeping')


stu = Student('张三', '男', 22)
print(stu.Name,stu.Sex,stu.Age) # 张三 男 22
print(stu.__dict__) # {'Name': '张三', 'Sex': '男', 'Age': 22}