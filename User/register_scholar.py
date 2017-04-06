# -*- coding:utf-8 -*-
import MySQLdb

def scholar_register(UNAME,PWD,MAIL,AGE,GENDER,NATION,CITY,INST,TTYPE,USERTYPE,MONEY=0):
    AGE = int(AGE)

    db = MySQLdb.connect("localhost","root","dbpjdbpj","ScholarDB")
    cursor = db.cursor()
# 邮箱是否已注册？
    sql = 'SELECT MAIL FROM USERINFO WHERE MAIL ="%s"' % MAIL
    cursor.execute(sql)
    if cursor.fetchall():
        db.close()
        return (False,"Mail already registered")

    sql = 'SELECT MAX(UNO) FROM USERINFO'
    cursor.execute(sql)
    max_uno = cursor.fetchall()[0][0] #return ((1000L,),)

    new_uno = max_uno + 1
    sql1 = "INSERT INTO USERINFO(UNO,UNAME,MAIL,AGE,USERTYPE,GENDER,NATION,CITY,MONEY,PWD)" \
          "VALUES(%d,'%s','%s',%d,'%s','%s','%s','%s',%d,'%s')" % (new_uno,UNAME,MAIL,AGE,USERTYPE,GENDER,NATION,CITY,0,PWD)
    sql2 = "INSERT INTO SCHOLAR(UNO,TYPE,INST,RATE) VALUES(%d,'%s','%s',%d)" % (new_uno,TTYPE,INST,1)
    print sql1,sql2
    try:
        cursor.execute(sql1)
        print 1
        cursor.execute(sql2)
        print 2
        db.commit()
        db.close()
        return (True,'Success')
    except:
        print 'fail'
        db.rollback()
        db.close()
        return (False,'Unknown reason')


