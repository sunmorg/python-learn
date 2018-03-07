# -*- coding:utf-8 -*-
# Author：sunmorg

age_of_sunm = 18

guess_age = int(input("guess age:"))

if age_of_sunm == guess_age:
    print("yes you got it")
elif guess_age > age_of_sunm:
    print("think smaller...")
else:
    print("think bigger...")