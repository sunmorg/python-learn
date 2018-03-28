# -*- coding:utf-8 -*-
# Author：sunmorg

from tabulate import tabulate

DB_FILE = 'staff_table.txt'
COLUMNS = ['id','name','age','phone','dept','enrolled_date']

def print_log(msg,log_type='info'):
    if log_type == 'info':
        print(msg)
    elif log_type == 'error':
        print('\033[31;1m%s\033[0m'%msg)

def load_db(dbfile):
    '''
    加载问件 并处理好数据 转成指定的格式
    :return:
    '''
    data = {}
    for i in COLUMNS:
        data[i] = []

    f = open(dbfile,'r')
    for line in f:
        staff_id,name,age,phone,dept,enrolled_date = line.split(',')
        data['id'].append(staff_id)
        data['name'].append(name)
        data['age'].append(age)
        data['phone'].append(phone)
        data['dept'].append(dept)
        data['enrolled_date'].append(enrolled_date)
    return data

STAFF_DATA = load_db(DB_FILE)

def op_gt(column,condtion):
    '''
    :param column:
    :param condtion:
    :return:
    '''
    marched_records = []
    for index,val in enumerate(STAFF_DATA[column]):
        if float(val) > float(condtion):
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            marched_records.append(record)
    return marched_records

def op_lt(column,condtion):
    marched_records = []
    for index, val in enumerate(STAFF_DATA[column]):
        if float(val) < float(condtion):
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            marched_records.append(record)
    return marched_records

def op_eq(column,condtion):
    marched_records = []
    for index, val in enumerate(STAFF_DATA[column]):
        if val == condtion:
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            marched_records.append(record)
    return marched_records

def op_link(column,condtion):
    marched_records = []
    for index, val in enumerate(STAFF_DATA[column]):
        if condtion in val:
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            marched_records.append(record)
    return marched_records

def syntax_where(clause):
    '''
    解析where条件，并且过滤
    :param clause:  eg：age>22
    :return:
    '''
    operators = {
        '>': op_gt,
        '<': op_lt,
        '=': op_eq,
        'link': op_link
    }
    for op_key,op_func in operators.items():
        if op_key in clause:
            column, condtion = clause.split(op_key)
            matched_data = op_func(column.strip(),condtion.strip())
            return matched_data
    else:
        print_log('\033[31;1m语法错误：where条件只能支持[>,<,=,link]\033[0m\n[find\\add\del\\update] [columnl,..] from [staff_table] [where] [column][>,...][condtion]','error')

def syntax_find(date_set,query_clause):
    '''
    解析查询语句 并从data_set中打印指定的列
    :param date_set:
    :param query_clause:
    :return:
    '''
    filter_cols_tmp = query_clause.split('from')[0][4:].split(',')
    filter_cols = [i.strip() for i in filter_cols_tmp]
    reformat_data_set = []
    for row in  date_set:
        filtered_vals = []
        for col in filter_cols:
            col_index = COLUMNS.index(col)
            filtered_vals.append(row[col_index])
        reformat_data_set.append(filtered_vals)
    # for r in reformat_data_set:
    #     print(r)
    print(tabulate(reformat_data_set,headers=filter_cols,tablefmt='grid'))

def syntax_delete(date_set,query_clause):
    pass

def syntax_update(date_set, query_clause):
    pass

def syntax_add(date_set, query_clause):
    pass

def syntax_parser(cmd):
    '''
    解析语句 并执行
    1,
    2,
    :param cmd:
    :return:
    '''
    syntax_list = {
        'find': syntax_find,
        'del': syntax_delete(),
        'add': syntax_add(),
        'update': syntax_update()
    }

    if cmd.split()[0] in ['find','add','del','update']:
        query_clause,where_clause = cmd.split('where')

        matched_records =syntax_where(where_clause)
        cmd_action = query_clause.split()[0]
        if cmd_action in syntax_list:
            syntax_list[cmd_action](matched_records, query_clause)



    else:
        print_log('语法错误：\n[find\\add\del\\update] [columnl,..] from [staff_table] [where] [column][>,...][condtion]','error')



def main():
    '''
    让用户输入语句， 并执行
    :return:
    '''
    while True:
        cmd = input("[staff_table]:").strip()
        if not cmd: continue
        syntax_parser(cmd.strip())

main()