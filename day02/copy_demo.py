# -*- coding:utf-8 -*-
# Author：sunmorg

import copy

person = ["name",["a",100]]

person1 = copy.copy(person)

person2 = person[:]

person3 = list[person]

print(person)

print(person1)

print(person2)

print(person3)