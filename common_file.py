#encoding=utf-8
import MySQLdb
def connect_db(user = 'root',pwd = 'dbpjdbpj',db = 'ScholarDB'):
    return MySQLdb.connect("localhost",user,pwd,db,charset = 'utf8')
