# -*- coding:utf-8 -*-
# Author：sunmorg

import getpass

_username = "sunm"

_password = "abc123"

username = input("name:")

password = getpass.getpass("password:")

if _username == username and _password == password :
    print("welcome user {name} login...".format(name = username))
else:
    print("invalid username or password")
