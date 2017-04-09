#encoding=utf-8
import MySQLdb

def connect_db():
    return MySQLdb.connect("localhost","root","dbpjdbpj","ScholarDB",charset = 'utf8')

def register(UNAME,PWD,MAIL,AGE,GENDER,NATION,CITY,INST,TTYPE,USERTYPE,MONEY=0):
    AGE = int(AGE)
    db = connect_db()
    cursor = db.cursor()
# 邮箱是否已注册？
    sql = 'SELECT MAIL FROM USERINFO WHERE MAIL ="%s"' % MAIL
    cursor.execute(sql)
    if cursor.fetchall():
        db.close()
        return (False,"Mail already registered")

    sql = 'SELECT MAX(UNO) FROM USERINFO'
    cursor.execute(sql)
    try:
        max_uno = cursor.fetchall()[0][0] #return ((1000L,),)
    except:
        max_uno = 1000

    new_uno = max_uno + 1
    sql1 = "INSERT INTO USERINFO(UNO,UNAME,MAIL,AGE,USERTYPE,GENDER,NATION,CITY,MONEY,PWD)" \
          "VALUES(%d,'%s','%s',%d,'%s','%s','%s','%s',%d,'%s')" % (new_uno,UNAME,MAIL,AGE,USERTYPE,GENDER,NATION,CITY,0,PWD)
    if USERTYPE == 'Scholar':
        sql2 = "INSERT INTO SCHOLAR(UNO,TYPE,INST,RATE) VALUES(%d,'%s','%s',%d)" % (new_uno,TTYPE,INST,1)
    elif USERTYPE == 'Volunteer':
        sql2 = "INSERT INTO VOLUNTEER(UNO,CRED) VALUES(%d,%d)" % (new_uno,100)
    else:
        raise ValueError('Unknown usertype: %s' % USERTYPE)

    print sql1,sql2
    try:
        cursor.execute(sql1)
        print 1
        cursor.execute(sql2)
        print 2
        db.commit()
        db.close()
        return (True,'Success')
    except Exception as e:
        print 'fail'
        db.rollback()
        db.close()
        print e.args
        return (False,'Unknown reason')


def login_id(UNO,PWD):
    db = connect_db()
    cursor = db.cursor()
    sql = 'SELECT PWD FROM USERINFO WHERE UNO = %d' % int(UNO)
    cursor.execute(sql)
    l = cursor.fetchall()
    if not l or l[0][0] != PWD:
        db.close()
        return (False,'Incorrect username or password')
    else:
        db.close()
        return (True,'Success')

def login_mail(MAIL,PWD):
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

def get_name(MAIL):
    db = connect_db()
    cursor = db.cursor()
    sql = 'SELECT UNAME FROM USERINFO WHERE MAIL = "%s"' % MAIL
    cursor.execute(sql)
    try:
        username = cursor.fetchall()[0][0]
        db.close()
        return username
    except KeyError:
        db.close()
        print "Not found"
        return ''
