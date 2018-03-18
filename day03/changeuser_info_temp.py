# -*- coding:utf-8 -*-
# Author：sunmorg

def prompt_func():
    return ('''
    欢迎来到员工信息查询系统！
    操作选项：
    1、模糊查询员工信息
    2、新增员工信息
    3、删除指定员工信息
    4、修改员工信息
    5、quit返回上一级
    ''')

def initial_employee_information():
    '''
    初始化员工信息数据,即把员工信息读到内存里面
    :return:{'id': ['1', '2', '4', '5', '6', '7', '8', '9', '10'], 'name': ['Alex Li', 'Jack Wang', 'Mack Qiao', 'Rachel Chen', 'Eric Liu', 'Chao Zhang', 'Kevin Chen', 'Shit Wen', 'Shanshan Du'], 'age': ['22', '28', '44', '23', '19', '21', '22', '20', '26'], 'phone': ['13651054608', '13451024608', '15653354208', '13351024606', '18531054602', '13235324334', '13151054603', '13351024602', '13698424612'], 'depart': ['IT', 'HR', 'Sales', 'IT', 'Marketing', 'Administration', 'Sales', 'IT', 'Operation'], 'enrolled_date': ['2013-04-01\n'', '2015-01-07\n'', '2016-02-01\n'', '2013-03-16\n'', '2012-12-01\n'', '2011-08-08\n'', '2013-04-01\n'', '2017-07-03\n'', '2017-07-02']}
    '''
    data_staff = {}
    staff_list = ['id', 'name', 'age', 'phone', 'depart', 'enrolled_date']
    for i in staff_list:
        data_staff[i] = []
    # print_log(data_staff)
    staff_infofile = open('staff_table.txt','r+',encoding='utf-8')
    for line in staff_infofile:
        print(line)
        staff_id, staff_name, staff_age, staff_phone, staff_depart, staff_date = line.split(',')
        data_staff['id'].append(staff_id)
        data_staff['name'].append(staff_name)
        data_staff['age'].append(staff_age)
        data_staff['phone'].append(staff_phone)
        data_staff['depart'].append(staff_depart)
        data_staff['enrolled_date'].append(staff_date)
    staff_infofile.close()
    return data_staff
DATA_STAFF = initial_employee_information()

def find_func():
    while True:
        print('''
    ***************************************************
                        命令行示例：
    find name age where age > 20
    find * from staff_table where dept IT
    find * from staff_table where enroll_date like 2013
    ***************************************************
            ''')
        user_input = input("请输入您要查询员工信息的正确的语法(如果想返回上一层，请按q):").split()
        for index,age in enumerate(DATA_STAFF['age']):
            if '>' in user_input:
                if age > user_input[-1]:
                    print(DATA_STAFF['name'][index],DATA_STAFF['age'][index])
            elif '<' in user_input:
                if age < user_input[-1]:
                    print(DATA_STAFF['name'][index],DATA_STAFF['age'][index])
            elif '=' in user_input:
                if age == user_input[-1]:
                    print(DATA_STAFF['name'][index],DATA_STAFF['age'][index])
        for index,depart in enumerate(DATA_STAFF['depart']):
            if depart in user_input:
                print(DATA_STAFF['id'][index], DATA_STAFF['name'][index],
                      DATA_STAFF['age'][index],DATA_STAFF['phone'][index],
                      DATA_STAFF['depart'][index], DATA_STAFF['enrolled_date'][index])
        for index,enrolled_date in enumerate(DATA_STAFF['enrolled_date']):
            enrolled_date =enrolled_date.split('-')[0]
            if enrolled_date in user_input and 'like' in user_input:
                print(DATA_STAFF['id'][index], DATA_STAFF['name'][index],
                      DATA_STAFF['age'][index],DATA_STAFF['phone'][index],
                      DATA_STAFF['depart'][index], DATA_STAFF['enrolled_date'][index])
        if user_input == 'q'.split():
            break

def add_func():
    while True:
        print('''   
        ***************************************************************
        员工录入示例：add staff_table Alex Li,25,134435344,IT,2015-10-29
        ***************************************************************
            ''')
        staff_infofile = open('staff_table.txt','a+',encoding='utf-8')
        user_input = input("请输入您要增加员工信息的正确的语法(如果想返回上一层，请按q):\n").split('staff_table')
        if user_input == 'q'.split():
            break
        core_message = ','.join(user_input)
        core_message =core_message.split(',')[1:]
        STAFF_ID = int(DATA_STAFF['id'][-1]) +1
        DATA_STAFF['id'].append(STAFF_ID)
        for iphone in DATA_STAFF['phone']:
            if core_message[2] ==iphone:
                print("手机不允许重复，请重新添加")
                add_func()
            else:
                pass
        staff_infofile.write('\n' + str(STAFF_ID) + ',' + ','.join(core_message))
        staff_infofile.close()
        print('\033[1;31m 影响了1条记录 \033[0m')

def del_func():
    print('''
        ***********************************
        删除示例：del from staff where  id=3
        ***********************************
        ''')
    del_staffid = input("请输入您要删除的员工id的语法:\n ")
    if  len(del_staffid) ==26 or len(del_staffid) ==27:
        del_staffid = del_staffid.split('=')
        count = 1
        del_left, del_right = del_staffid
        if del_right in DATA_STAFF['id']:
            staff_index = DATA_STAFF['id'].index(del_right)
            staff_infofile = open('staff_table.txt', 'w', encoding='utf_8')
            print('\033[31;1m员工 ' + DATA_STAFF['name'][staff_index] + ' 已经删除\033[0m')
            del DATA_STAFF['id'][staff_index]
            del DATA_STAFF['name'][staff_index]
            del DATA_STAFF['age'][staff_index]
            del DATA_STAFF['phone'][staff_index]
            del DATA_STAFF['depart'][staff_index]
            del DATA_STAFF['enrolled_date'][staff_index]
            while True:
                staff_wr = DATA_STAFF['id'][count] + ',' + DATA_STAFF['name'][count] + ',' + DATA_STAFF['age'][count] + ',' + DATA_STAFF['phone'][count] + ',' + DATA_STAFF['depart'][count] + ',' + DATA_STAFF['enrolled_date'][count]
                staff_infofile.write(staff_wr)
                count += 1
                if count == len(DATA_STAFF['id']):
                    break
            staff_infofile.close()
        else:
            print("\033[31;1m员工信息表中无此员工的信息，请重新输入\033[0m")
            del_func()

    else:
        print("\033[31;1m输入的语法有误，请重输！\33[0m")
        del_func()
    print('\033[1;31m 影响了1条记录 \033[0m')
def update_func():
    print('''
        *************************************************************
        示例:UPDATE staff_table SET dept="Market" WHERE  dept = "IT"
            UPDATE staff_table SET age=25 WHERE  name = "Alex Li"
        *************************************************************
        ''')
    update_staff = input("请输入您要更新的员工信息的语法:\n ")
    user_update = update_staff.split('SET')
    update_staff_left,update_staff_right = user_update
    user_update_finally = user_update[-1].strip().split('WHERE')
    after_update = user_update_finally[0]
    before_update = user_update_finally[1]
    after_update_name,after_update_content = after_update.split('=')
    before_update_name, before_update_content = before_update.split('=')
    if after_update_name.strip() == before_update_name.strip():
        for dept in DATA_STAFF['depart']:
            if dept == eval(before_update_content):
                DATA_STAFF['depart'][DATA_STAFF['depart'].index(eval(before_update_content))] = eval(after_update_content)
        count = 0
        staff_infofile = open('staff_table.txt', 'w', encoding='utf_8')
        while True:
            staff_wr = DATA_STAFF['id'][count] + ',' + DATA_STAFF['name'][count] + ',' + DATA_STAFF['age'][count] + ',' + DATA_STAFF['phone'][count] + ',' + DATA_STAFF['depart'][count] + ',' + DATA_STAFF['enrolled_date'][count]
            staff_infofile.write(staff_wr)
            count += 1
            if count == len(DATA_STAFF['id']):
                break
        staff_infofile.close()
        print('\033[1;31m 影响了3条记录 \033[0m')
    else:
        for index,name in enumerate(DATA_STAFF['name']):
            if name.strip() == eval(before_update_content).strip():
                DATA_STAFF['age'][index] = eval(after_update_content)
            else:
                pass
        count = 0
        staff_infofile = open('staff_info.txt', 'w', encoding='utf_8')
        while True:
            staff_wr = str(DATA_STAFF['id'][count]) + ',' + DATA_STAFF['name'][count] + ','                        + str(DATA_STAFF['age'][count]) + '','' + str(DATA_STAFF['phone'][count]) + '',''                        + DATA_STAFF['depart'][count] + '','' + DATA_STAFF['enrolled_date'][count]
            staff_infofile.write(staff_wr)
            count += 1
            if count == len(DATA_STAFF['id']):
                break
        staff_infofile.close()
        print('\033[1;31m 影响了1条记录 \033[0m')

def main():
    while True:
        print(prompt_func())
        user_input = input("请输入要执行操作的序号>>  ")
        if user_input == '1':
            print("-------------欢迎进入模糊查询员工信息界面----------------")
            find_func()
        elif user_input == '2':
            print("-------------欢迎进入新增员工信息界面----------------")
            add_func()
        elif user_input == '3':
            print("-------------欢迎进入删除指定员工信息界面----------------")
            del_func()
        elif user_input == '4':
            print("-------------欢迎进入修改员工信息界面----------------")
            update_func()
        else:
            print("\033[31;1m输入的信息有误，请重输！\33[0m")

if __name__ == '__main__':
    main()