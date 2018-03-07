# -*- coding:utf-8 -*-
# Author：sunmorg

name = input("name?")

age = int(input("age?")) #int()把数据类型转换成整型 str()把数据类型转换成字符串类型

print(type(age))

job = input("job?")

salary = input("salary?")

print(name,age)

'''

    %s表示字符串
    %d表示整数
    %f表示浮点数

'''

info = '''
------------------ info of %s ------------------
                name: %s
                age: %d
                job: %s
                salary: %s
''' % (name, name, age, job, salary)

print(info)

info2 = '''
------------------ info2 of {_name} ------------------
                name: {_name}
                age: {_age}
                job: {_job}
                salary: {_salary}
'''.format(_name=name,_age=age,_job=job,_salary=salary)

print(info2)

info3 = '''
------------------ info3 of {0} ------------------
                name: {0}
                age: {1}
                job: {2}
                salary: {3}
'''.format(name,age,job,salary)

print(info3)