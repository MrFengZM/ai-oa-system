import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a complex string'  # 用于签名的安全密钥
    DB_HOST = '192.168.40.10'  # 数据库主机地址
    DB_USER = 'root'  # 数据库用户名
    DB_PASSWORD = '123'  # 数据库密码
    DB_NAME = 'oa'  # 数据库名称
    DB_PORT = 3386