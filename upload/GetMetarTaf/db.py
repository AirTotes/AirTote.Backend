from mysql.connector import connect, MySQLConnection
from configparser import ConfigParser
from os import environ

cfg = ConfigParser()
cfg.read(environ['HOME'] + '/.airtote.backend/config.ini', 'UTF-8')

CFG_MYSQL = 'mysql'
CFG_DB_NAME = 'db_name'
CFG_DB_HOST = 'db_host'
CFG_DB_USER = 'db_user'
CFG_DB_PASSWORD = 'db_password'

def getConnection() -> MySQLConnection:
  return connect(
    user = cfg.get(CFG_MYSQL, CFG_DB_USER),
    password = cfg.get(CFG_MYSQL, CFG_DB_PASSWORD),
    host = cfg.get(CFG_MYSQL, CFG_DB_HOST),
    database = cfg.get(CFG_MYSQL, CFG_DB_NAME)
  )
