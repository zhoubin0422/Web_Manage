#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zhoubin
# Date: 2019/1/24
# Description:

import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from modules import backup


msg = """
    请输入你想进行的操作：
    1. 备份网站数据：python main.py backupweb
    2. 完全备份数据库：python main.py backupdb db_name(如果不输入，则默认为备份所有数据库)
"""


def main():
    sys.argv.append("")
    if sys.argv[1] == 'backupweb':
        obj = backup.BackupWeb()
        obj.backup_web()
    elif sys.argv[1] == 'backupdb':
        obj = backup.BackupDB()
        if sys.argv[1] == 'backupdb' and sys.argv[2]:
            obj.full_backup(sys.argv[2])
        elif sys.argv[1] == 'backupdb' and sys.argv[2] == '':
            obj.full_backup('')
        elif sys.argv[1] == 'backupdb' and sys.argv[2] == '2':
            obj.increment_backup()
    else:
        print(msg)


if __name__ == '__main__':
    main()