# -*- coding:utf-8 -*-
# Author：sunmorg

# age_of_sunm = 18
#
# for i in range(3):
#     guess_age = int(input("guess age:"))
#     if age_of_sunm == guess_age:
#         print("yes you got it")
#         break
#     elif guess_age > age_of_sunm:
#         print("think smaller...")
#     else:
#         print("think bigger...")
# else:
#     print("you have tried too many times...")

# for i in range(0,10,4):
#     print("loop...",i)


#continue 跳出本次循环 进入下次循环  break 结束整个循环
# for i in range(0,10):
#     if i < 3:
#         print("loop...",i)
#     else:
#         continue
#     print("continue.......")


for i in range(10):
    print(".......",i)
    for j in range(10):
        print(j)
        if j > 5:
            break