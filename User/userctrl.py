# encoding=utf-8
import MySQLdb
from common_file import connect_db

def grant_scholar(uno,pwd,cursor,db):
    cursor.execute("CREATE USER scholar_%d IDENTIFIED by '%s'" % (uno, pwd))
    cursor.execute("GRANT SELECT,DELETE,UPDATE,INSERT ON ScholarDB.* TO scholar_%d" % uno)
    cursor.execute("CREATE DATABASE WorkSpace_%d" % uno)
    cursor.execute("GRANT SELECT,DELETE,UPDATE,INSERT ON WorkSpace_%d.* to scholar_%d" % (uno,uno))
    db.commit()
    db2 = connect_db('root','dbpjdbpj','WorkSpace_%d' % uno)
    cursor2 = db2.cursor()
    cursor2.execute("create table PRIV_QUESTION(\
    QNO INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,\
    TITLE VARCHAR(200) NOT NULL,\
    SUPPLEMENT VARCHAR(200),\
    SUPPLEMENT_TYPE VARCHAR(45),\
    TYPE VARCHAR(45) NOT NULL,\
    INPUTTYPE VARCHAR(45) NOT NULL\
    )")
    cursor2.execute("create table PRIV_CHOICE(\
        CNO INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,\
        PLACE INTEGER NOT NULL,\
        QNO INTEGER NOT NULL,\
        CONTENT VARCHAR(200)\
    )")
    db2.commit()
    db2.close()

def grant_volunteer(uno,pwd,cursor,db):
    cursor.execute("CREATE USER volunteer_%d IDENTIFIED by '%s'" % (uno, pwd))
    cursor.execute("GRANT SELECT,DELETE,UPDATE,INSERT ON ScholarDB.* TO scholar_%d" % uno)
    db.commit()

def register(UNAME, PWD, MAIL, AGE, GENDER, NATION, CITY, INST, TTYPE, USERTYPE, MONEY=0):
    AGE = int(AGE)
    db = connect_db()
    cursor = db.cursor()
    # 邮箱是否已注册？
    sql = 'SELECT MAIL FROM USERINFO WHERE MAIL ="%s"' % MAIL
    cursor.execute(sql)
    if cursor.fetchall():
        db.close()
        return (False, "Mail already registered")

    sql = 'SELECT MAX(UNO) FROM USERINFO'
    cursor.execute(sql)

    max_uno = cursor.fetchall()[0][0]  # return ((1000L,),)
    try:
        new_uno = max_uno + 1
    except TypeError:
        new_uno = 1000
    sql1 = "INSERT INTO USERINFO(UNO,UNAME,MAIL,AGE,USERTYPE,GENDER,NATION,CITY,MONEY,PWD)" \
           "VALUES(%d,'%s','%s',%d,'%s','%s','%s','%s',%d,'%s')" % (
               new_uno, UNAME, MAIL, AGE, USERTYPE, GENDER, NATION, CITY, 0, PWD)
    if USERTYPE == 'Scholar':
        sql2 = "INSERT INTO SCHOLAR(UNO,TYPE,INST,RATE) VALUES(%d,'%s','%s',%d)" % (new_uno, TTYPE, INST, 1)
    elif USERTYPE == 'Volunteer':
        sql2 = "INSERT INTO VOLUNTEER(UNO,CRED) VALUES(%d,%d)" % (new_uno, 100)
    else:
        raise ValueError('Unknown usertype: %s' % USERTYPE)

    #print sql1, sql2
    cursor.execute(sql1)
    #print 1
    cursor.execute(sql2)
    #print 2
    # update
    #if USERTYPE == 'Scholar':
    #    grant_scholar(new_uno,PWD,cursor,db)
    db.commit()
    db.close()
    return True, 'Success'

def login_mail(MAIL, PWD):
    db = connect_db()
    cursor = db.cursor()
    sql = 'SELECT PWD FROM USERINFO WHERE MAIL = "%s"' % MAIL
    cursor.execute(sql)
    l = cursor.fetchall()
    if not l or l[0][0] != PWD:
        db.close()
        return (False, '用户名或者密码不正确')
    else:
        db.close()
        return (True, 'Success')


def get_basic_info(MAIL):
    db = connect_db()
    cursor = db.cursor()
    sql = 'SELECT UNAME,UNO,USERTYPE FROM USERINFO WHERE MAIL = "%s"' % MAIL
    cursor.execute(sql)
    try:
        username,uno,usertype = cursor.fetchall()[0][0:3]
        db.close()
        return username,uno,usertype
    except KeyError:
        db.close()
        #print "Not found"
        return ''

def get_money(UNO):
    uno = int(UNO)
    db = connect_db()
    cursor = db.cursor()
    sql = 'SELECT MONEY FROM USERINFO WHERE UNO = %d'% uno
    cursor.execute(sql)
    money = cursor.fetchone()[0]
    db.close()
    return money