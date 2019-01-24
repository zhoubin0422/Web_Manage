# 项目说明
## 环境需求
* Python 版本：Python 3.6.x
* 系统：CentOS / Redhat

## 需要用到的第三方模块:
* pyyaml

## 目录结构如下
```bash
.
├── bin
│   ├── __init__.py
│   ├── main.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   └── start.cpython-36.pyc
├── conf
│   ├── base.example.cnf
│   └── logging.conf.yaml
├── logs
│   └── backup.log
├── manage.py
├── modules
│   ├── backup.py
│   ├── __init__.py
│   └── __pycache__
│       ├── backup.cpython-36.pyc
│       └── __init__.cpython-36.pyc
└── README.md
```

### 项目目录说明
* bin： 目录下的 main.py 为程序主入口
* conf： 目录为配置文件所在目录
* logs： 为程序运行时产生的日志文件存放目录
* modules： 存放功能模块的目录
* manage.py：项目程序入口文件

## 项目已经实现的功能
* 备份网站数据
* 全量备份MySQL数据库（mysqldump）


## 项目安装
* 下载项目
```bash
git clone https://github.com/zhoubin0422/Web_Manage.git
```

* 创建配置文件 base.cnf
```bash
cd Web_Manage/conf
cp base.ezample.cnf base.cnf

# 修改其中对应的配置参数
```

* 安装第三方模块 pyyaml
```bash
pip install pyyaml
```

## 项目使用
* 备份网站数据
```bash
cd Web_Manage
python manage.py backupweb
```

* 备份MySQL数据库中所有的库
```bash
cd Web_Manage
python manage.py backupdb

```

* 备份MySQL数据库的指定的库
```bash
cd Web_Manage
python manage.py backupdb mysite  # mysite 为需要备份的数据库名字
```
