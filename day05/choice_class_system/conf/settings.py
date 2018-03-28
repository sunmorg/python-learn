# -*- coding:utf-8 -*-
# Author：sunmorg

#!/usr/bin/env python
# -*- coding:utf-8 -*-
#-Author-Lian

import os
import sys
import platform

if platform.system() == "Windows":
    BASE_DIR = "\\".join(os.path.abspath(os.path.dirname(__file__)).split("\\")[:-1])
    database_path = os.path.join(BASE_DIR,"database")

else:
    BASE_DIR = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
    database_path = os.path.join(BASE_DIR, "database")

school_db_file = os.path.join(database_path,"school")
