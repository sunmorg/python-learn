#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/2/4 14:22.
 * @author: Chinge_Yang.
'''

import sys
import re
from core import logger

'''
思路：
1. 先把小括号里不包含小括号的算式获取出来，算出结果，用结果把算式替换；
2. 循环1直到替换小括号得到的结果无小括号为止；
3. 1是调用加减乘除来得到无括号的算术结果；
'''


def filter_brackets(expression):
    """
     过滤出第一个最优先小括号中的算式，并计算出结果，把结果替换小括号
    :param expression: 表达式
    :return: 递归处理
    """
    re_brackets = re.compile(r'\(([^()]+)\)')
    if not re_brackets.search(expression):  # 判断小括号，如果不存在小括号，直接调用乘除，加减计算
        ret1 = multiply_divided(expression)  # 第一步，先计算乘除
        ret2 = plus_minus(ret1)  # 第二步，计算加减
        return ret2  # 返回最终计算结果

    exp_group = re_brackets.search(expression).group()  # 如果有小括号，匹配出优先级最高的小括号
    exp_group = exp_group.strip('[\(\)]')  # 删除小括号
    ret1 = multiply_divided(exp_group)  # 计算乘除
    ret2 = plus_minus(ret1)  # 计算加减
    part1, replace_str, part2 = re_brackets.split(expression, 1)  # 将小括号计算结果替换回表达式
    expression = '%s%s%s' % (part1, ret2, part2)  # 生成新的表达式
    return filter_brackets(expression)  # 递归去小括号，然后处理


def multiply_divided(expression):
    """
    乘除运算
    :param expression: 表达式
    :return: 返回没有乘除的表达式/最终计算结果
    """
    mul_div = re.compile('\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*')
    flag = mul_div.search(expression)  # 匹配乘除号
    if not flag:  # 乘除号不存在，返回输入的表达式
        return expression

    data = flag.group()  # 匹配乘除号
    if '*' in data:  # 当可以用乘号分割，证明有乘法运算
        part1, part2 = data.split('*')  # 以乘号作为分割符获取2部分算式
        value = float(part1) * float(part2)  # 计算乘法
    else:
        part1, part2 = data.split('/')  # 用除号分割
        if float(part2) == 0:  # 如果分母为0，则退出计算
            sys.exit("Do not allow the divisor is 0!")
        value = float(part1) / float(part2)  # 计算除法

    # 获取第一个匹配到的乘除计算结果value，将value放回原表达式
    s1, s2 = mul_div.split(expression, 1)  # 分割表达式
    # print("上一个表达式：",expression)
    next_expression = "%s%s%s" % (s1, value, s2)  # 将计算结果替换会表达式
    # print("下一个表达式%s" % next_expression)
    return multiply_divided(next_expression)  # 递归表达式


def plus_minus(expression):
    '''
    :param expression: 表达式
    :return:
    '''
    expression = expression.replace('+-', '-')  # 替换表达式里的所有'+-'
    expression = expression.replace('--', '+')  # 替换表达式里的所有'--'
    expression = expression.replace('-+', '-')  # 替换表达式里的所有'-+'
    expression = expression.replace('++', '+')  # 替换表达式里的所有'++'

    plu_min = re.compile('[\-]?\d+\.*\d*[\+\-]{1}\d+\.*\d*')  # 正则匹配加减号

    # print("处理特殊加减后的表达式：",expression)
    flag = plu_min.search(expression)  # 匹配加减号
    if not flag:  # 如果不存在加减号，则证明表达式已计算完成，返回最终结果
        return expression

    data = flag.group()
    if len(data.split('+')) > 1:  # 以加号分割成功，有加法计算
        part1, part2 = data.split('+')
        value = float(part1) + float(part2)  # 计算加法
    elif data.startswith('-'):  # 如果是以'-'开头则需要单独计算
        part1, part2, part3 = data.split('-')
        value = -float(part2) - float(part3)  # 计算以负数开头的减法
    else:
        part1, part2 = data.split('-')
        value = float(part1) - float(part2)  # 计算减法

    s1, s2 = plu_min.split(expression, 1)  # 分割表达式
    next_expression = "%s%s%s" % (s1, value, s2)  # 将计算后的结果替换回表达式，生成下一个表达式
    return plus_minus(next_expression)  # 递归运算表达式


def input_func():
    """
    输入判断
    :param expression: 表达式
    :return: 返回有效表达式
    """
    while True:
        expression = input("Please input your expression[\033[32;1mq\033[0m to quit]：").strip()
        if expression == 'q':  # 退出
            sys.exit("Bye bye".center(50, '*'))
        elif len(expression) == 0:
            continue
        elif re.match("[a-z]+", expression, flags=re.IGNORECASE):   # 包括字母，程序会出现变量未定义退出
            print("\033[31;1mThe input expression is not correct, please input again!\033[0m")
            continue
        else:
            expression = re.sub('\s*', '', expression)  # 去除空格
            return expression


def run():
    exit_flag = False
    print("Welcome to calculator!".center(50, '*'))
    while exit_flag is not True:
        try:
            expression = input_func()  # 获取到的表达式
            ret = float(filter_brackets(expression))  # 用函数计算后得出的结果
            result = float(eval(expression))  # 用eval计算验证
            if result == ret:  # 将两种方式计算的结果进行比较，如果相等，则计算正确，输出结果
                print("The expression result：%s" % ret)
            else:  # 两种计算方式的结果不正确，提示异常，并返回两种方式的计算结果
                print("The expression correct result：\033[32;1m%s\033[0m" % result)
                print("The expression of calculator result：\033[31;1m%s\033[0m" % ret)

            log_type = "history"  # 历史记录记录到文件中
            history_logger = logger.logger(log_type)
            history_logger.info("Expression: %s=%s" %(expression, ret))
        except(SyntaxError, ValueError, TypeError):  # 如果有不合法输出，则抛出错误
            print("\033[31;1mThe input expression is not correct, please check again!\033[0m")
        print("-".center(50, '-'))
