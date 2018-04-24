# -*- coding:utf-8 -*-
# Author：sunmorg

import configparser, os
from client import FtpClient

if __name__ == '__main__':
    ftp = FtpClient()
    ftp.connect('127.0.0.1', 9999)
    auth_tag = False
    while auth_tag != True:
        auth_tag = ftp.auth()
    ftp.interactive()