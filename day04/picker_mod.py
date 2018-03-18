# -*- coding:utf-8 -*-
# Author：sunmorg

import pickle

# d = {"name":"sunm","age":22}
#
# pk = open("data.pkl","wb")
#
# pickle.dump(d,pk)


f = open("data.pkl","rb")

d = pickle.load(f)

print(d)