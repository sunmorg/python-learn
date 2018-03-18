# -*- coding:utf-8 -*-
# Author：sunmorg

import configparser

conf = configparser.ConfigParser()

# print(conf.sections())

conf.read('conf.ini')
# print(conf.sections())
#
# print(conf.default_section)
#
# print(list(conf["topsecret.server.com"].keys()))
#
# print(conf["topsecret.server.com"]["host port"])

# for k,v in conf['topsecret.server.com'].items():
#     print(k,v)

# if 'forwardx11' in conf['topsecret.server.com']:
#     print('in')