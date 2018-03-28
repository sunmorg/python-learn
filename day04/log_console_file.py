# -*- coding:utf-8 -*-
# Author：sunmorg

import logging

logger = logging.getLogger("web")

console_handle = logging.StreamHandler()
file_handle = logging.FileHandler('web.log')

console_handle.setLevel(logging.DEBUG)

file_handle.setLevel(logging.WARNING)

logger.addHandler(console_handle)
logger.addHandler(file_handle)

file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)s - %(message)s')

console_handle.setFormatter(console_format)

file_handle.setFormatter(file_format)

logger.info("test log")
logger.error("test log")

