# -*- coding:utf-8 -*-
# Author：sunmorg

# def read_table():
#     f = open('staff_table.txt','r',encoding='utf-8')
#     for line in f:
#         line_data = line.strip()
#         line_data.split(',')
#         print()
# read_table()
#_*_coding:utf-8_*_
# !/user/bin/env python
import re
command_list = ['find', 'update', 'where', 'add', 'del']
def prompt_func():
    return ('''
    欢迎来到员工信息查询系统！
    操作选项：
    1、模糊查询
    2、创建新员工纪录
    3、删除指定员工信息纪录
    4、修改员工信息
    5、quit返回上一级
    6、exit退出程序
    ''')
def staff_data():
    ' 读取员工信息到内存 '
    data_staff = {}
    staff_list = ['id', 'name', 'age', 'phone', 'depart', 'enrolled_date']
    for staff_line in staff_list:
        data_staff[staff_line] = []
    staff_file = open('staff_table.txt', 'r+t', encoding='utf_8')
    for staff_information in staff_file:
        staff_id, staff_name, staff_age, staff_phone, staff_depart, staff_date = staff_information.split(',')
        data_staff['id'].append(staff_id)
        data_staff['name'].append(staff_name)
        data_staff['age'].append(staff_age)
        data_staff['phone'].append(staff_phone)
        data_staff['depart'].append(staff_depart)
        data_staff['enrolled_date'].append(staff_date)
    staff_file.close()
    return data_staff
DATA_STAFF = staff_data()
def where_func():
    while True:
        print('''
***************************************************
命令行示例：        
find name age where age > 20
find *from staff_table where dept IT
find *from staff_table where enroll_date like 2013      
***************************************************
        ''')
        user_cmd = input('>').split()
        count = 0
        for dex, age in enumerate(DATA_STAFF['age']):
            if '>' in user_cmd:
                if age > user_cmd[6]:
                    count += 1
                    print(DATA_STAFF['name'][dex], DATA_STAFF['age'][dex])
            elif '<' in user_cmd:
                if age < user_cmd[6]:
                    count += 1
                    print(DATA_STAFF['name'][dex], DATA_STAFF['age'][dex])
            elif '=' in user_cmd:
                if age == user_cmd[6]:
                    count += 1
                    print(DATA_STAFF['name'][dex], DATA_STAFF['age'][dex])
        for dex, depart in enumerate(DATA_STAFF['depart']):
            if depart in user_cmd:
                count += 1
                print(DATA_STAFF['id'][dex], DATA_STAFF['name'][dex], DATA_STAFF['age'][dex], DATA_STAFF['phone'][dex], \
                      DATA_STAFF['depart'][dex], DATA_STAFF['enrolled_date'][dex])
        for dex, enrolled_date in enumerate(DATA_STAFF['enrolled_date']):
            enrolled_date = enrolled_date.split('-')[0]
            if enrolled_date in user_cmd and 'like' in user_cmd:
                count += 1
                print(DATA_STAFF['id'][dex], DATA_STAFF['name'][dex], DATA_STAFF['age'][dex], DATA_STAFF['phone'][dex],
                      DATA_STAFF['depart'][dex], DATA_STAFF['enrolled_date'][dex])
        if user_cmd == 'quit'.split():
            break
        print('此次查询出%s条数据' %count)
def add_staff():
    while True:
        print('''       
    ***************************************************************
    员工录入示例：add staff_table Alex Li,25,134435344,IT,2015-10-29
    ***************************************************************
        ''')
        staff_file = open('staff_table.txt', 'at', encoding='utf_8')
        staff_user = input('>').split()
        if staff_user == 'quit'.split():
            break
        staff_user_right = staff_user[2:]
        print(staff_user_right)
        STAFF_ID = int(DATA_STAFF['id'][-1]) + 1
        DATA_STAFF['id'].append(STAFF_ID)
        staff_file.write('\n' + str(STAFF_ID) + ',' + str(staff_user_right[0])+staff_user_right[1])
        staff_file.close()

def del_func():
    print('''
    ***********************************
    删除示例：del from staff where  id=3
    ***********************************
    ''')
    count = 0
    user_del_input = input('>').split('=')
    del_left, del_right = user_del_input
    if del_right in DATA_STAFF['id']:
        staff_index = DATA_STAFF['id'].index(del_right)
        staff_file = open('staff_table.txt', 'w', encoding='utf_8')
        print('员工 ' + DATA_STAFF['name'][staff_index] + ' 已经删除')
        del DATA_STAFF['id'][staff_index]
        del DATA_STAFF['name'][staff_index]
        del DATA_STAFF['age'][staff_index]
        del DATA_STAFF['phone'][staff_index]
        del DATA_STAFF['depart'][staff_index]
        del DATA_STAFF['enrolled_date'][staff_index]
        while True:
            staff_wr = DATA_STAFF['id'][count] + ',' + DATA_STAFF['name'][count] + ',' + DATA_STAFF['age'][count] + ',' +\
                       DATA_STAFF['phone'][count] + ',' + DATA_STAFF['depart'][count] + ',' + DATA_STAFF['enrolled_date'][count]
            staff_file.write(staff_wr)
            count += 1

            if count == len(DATA_STAFF['id']):
                break
        staff_file.close()
def update_func():

    print('''
    *********************************************************
    示例: UPDATE staff_table SET dept=Marketing WHERE  dept=IT
    *********************************************************
    ''')
    user_update = input('>').split('WHERE')
    user_update_left, user_update_right = user_update
    update_count = 0
    for dept in DATA_STAFF['depart']:
        if dept in user_update_right:
            update_count +=1
            DATA_STAFF['depart'][DATA_STAFF['depart'].index(dept)] = user_update_left[28:].strip()
    count = 0
    staff_file = open('staff_table.txt', 'w', encoding='utf_8')
    while True:
        staff_wr = DATA_STAFF['id'][count] + ',' + DATA_STAFF['name'][count] + ',' + DATA_STAFF['age'][count] + ',' + \
                   DATA_STAFF['phone'][count] + ',' + DATA_STAFF['depart'][count] + ',' + DATA_STAFF['enrolled_date'][
                       count]
        staff_file.write(staff_wr)
        count += 1
        if count == len(DATA_STAFF['id']):
            break
        print('此次修改了%s条数据' % update_count)
    staff_file.close()
if __name__ == '__main__':
    while True:
        print(prompt_func())
        user_opt = input('选项:')
        if user_opt == '1':
            where_func()
        elif user_opt == '2':
            add_staff()
        elif user_opt == '3':
            del_func()
        elif user_opt == '4':
            update_func()
        elif user_opt == '6':
            exit()