#encoding=utf-8
import MySQLdb
def connect_db():
    return MySQLdb.connect("localhost","root","dbpjdbpj","ScholarDB",charset = 'utf8')
