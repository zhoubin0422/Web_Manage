#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zhoubin
# Date: 2019/1/24
# Description: 该模块主要用于编写web网站与MySQL数据库备份的方法

import os
import sys
import shutil
import subprocess
import tarfile
import configparser
import logging
import logging.config
import yaml
import time


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
BASE_CONF_FILE = os.path.join(BASE_DIR, 'conf', 'base.cnf')
LOGGING_CONF_FILE = os.path.join(BASE_DIR, 'conf', 'logging.conf.yaml')


class BaseClass(object):
    """
    这个类主要用于编写一些通用的方法与属性
    """
    def __init__(self):
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(BASE_CONF_FILE)
        self.web_data_dir = parser.get('Web', 'Web_Data_Dir')
        self.web_backup_dir = parser.get('Web', 'Web_Backup_Dir')
        self.mysql_backup_dir = parser.get('MySQL', 'mysql_backup_dir')
        self.mysql_binlog_dir = parser.get('MySQL', 'mysql_binlog_dir')
        self.mysql_user = parser.get('MySQL', 'user')
        self.mysql_password = parser.get('MySQL', 'password')
        self.mysql_host = parser.get('MySQL', 'host')
        self.mysql_port = parser.get('MySQL', 'port')

        with open(LOGGING_CONF_FILE, 'r') as f:
            dic = yaml.load(f)
            logging.config.dictConfig(dic)
        self.logger = logging.getLogger('Backup')

    def check_dir(self, path):
        """ 目录检查函数 """
        if os.path.isdir(path):
            if os.access(path, os.R_OK) and os.access(path, os.W_OK):
                self.logger.info('{} 已经存在！'.format(path))
                return True
            else:
                os.chmod(path, mode=os.R_OK)
                os.chmod(path, mode=os.W_OK)
                return True
        else:
            os.makedirs(path)
            return True

    # def loging(self):
    #     """ 日志处理函数 """
    #     return self.logger


class BackupWeb(BaseClass):
    """
    这个类用于备份网站目录数据
    """
    def backup_web(self):
        """ 该方法用于打包备份网站目录与文件 """
        if self.check_dir(self.web_backup_dir):
            start_date = time.strftime('%Y-%m-%d')
            file_name = 'Web_backup_{}.tar.gz'.format(start_date)

            try:
                os.chdir(self.web_data_dir)
                self.logger.info('正在打包文件...')
                tar = tarfile.open(file_name, 'w:gz')
                for root, dirs, files in os.walk(os.getcwd()):
                    for file in files:
                        full_path = os.path.join(root, file)
                        tar.add(full_path)
                tar.close()
                if os.path.exists(os.path.join(self.web_backup_dir, file_name)):
                    os.remove(os.path.join(self.web_backup_dir, file_name))
                shutil.move(file_name, self.web_backup_dir)
                self.logger.info('文件打包完成！！')
            except Exception as e:
                print(e)


class BackupDB(BaseClass):
    """
    这个类里面的方法主要用于备份 MySQL 数据库
    """
    def full_backup(self, db_name):
        """
        数据库全量备份方法
        :param db_name: 需要备份数据库名称
        :return:
        """
        if self.check_dir(self.mysql_backup_dir):
            if db_name:
                db_name = db_name
                flags = '--databases'
                file_name = '{}.sql'.format(db_name)
            else:
                db_name = ""
                flags = '--all-databases'
                file_name = 'all_databases.sql'
            start_date = time.strftime('%Y-%m-%d')
            tar_name = '{0}_{1}'.format(file_name, start_date)

            cmd = 'mysqldump -u{0} -p{1} ' \
                  '--single-transaction ' \
                  '--flush-logs ' \
                  '--master-data=2 ' \
                  '--routines ' \
                  '--triggers ' \
                  '--events ' \
                  '{2} {3} > {4}'.format(self.mysql_user, self.mysql_password, flags, db_name, file_name)

            try:
                self.logger.info('正在对数据库 {} 进行全量备份，请稍等...'.format(db_name))
                s = subprocess.run(cmd, shell=True)
                if s.returncode == 0:
                    shutil.make_archive(base_name=os.path.join(self.mysql_backup_dir, tar_name), format='gztar', base_dir=file_name)
                    os.remove(file_name)
                    self.logger.info('数据库 {} 备份完成！！'.format(db_name))
                else:
                    self.logger.error('数据库 {} 备份失败，请手动备份！！'.format(db_name))
            except Exception as e:
                self.logger.error(e)

    def increment_backup(self):
        """
        数据库增量备份方法
        """
        pass

