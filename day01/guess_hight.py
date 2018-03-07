# -*- coding:utf-8 -*-
# Author：sunmorg

count = 0

age_of_sunm = 18

while count < 3:
    guess_age = int(input("guess age:"))
    count = count + 1
    if age_of_sunm == guess_age:
        print("yes you got it")
        break
    elif guess_age > age_of_sunm:
        print("think smaller...")
    else:
        print("think bigger...")
    if count == 3:
        countine_confirm = input("do you want to keep guessing?")
        if countine_confirm != 'n':
            count = 0
# else:
#     print("you have tried too many times...")