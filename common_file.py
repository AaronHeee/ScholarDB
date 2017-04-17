#encoding=utf-8
import MySQLdb
def connect_db():
    return MySQLdb.connect("localhost","root","123456","ScholarDB",charset = 'utf8')
