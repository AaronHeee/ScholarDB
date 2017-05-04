#encoding=utf-8

import MySQLdb
import time
from common_file import connect_db


def add_survey_to_list(subject=None, user='root', pwd='dbpjdbpj'):

    sql = "SELECT SNO, TYPE, TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM SURVEY "
    condition = []
    if subject != [None] and subject != [''] and subject != []:
        for sub in subject:
            if sub == '' or sub == ' ':
                continue
            condition.append("SNO IN (SELECT SNO FROM SURVEY_SUBJECT WHERE WHAT = '%s')" % sub)
    if condition != None and condition != []:
        sql += ' WHERE '
        sql += ' AND '.join(condition)
        sql += ' AND '
    else :
        sql += ' WHERE '
    sql += " STAGE ='OPEN'"
    return sql

def add_task_to_list(datatype=None, user='root', pwd='dbpjdbpj'):

    sql = "SELECT TASK.TNO,TYPE,TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM TASK"
    if datatype != '' and datatype != None:
        sql += ",FILE,TASK_WITH_FILE WHERE TASK.TNO=TASK_WITH_FILE.TNO AND FILE.FNO=TASK_WITH_FILE.FNO AND FILE.DATATYPE='%s' AND" % datatype
    else:
        sql += " WHERE "
    sql += " STAGE = 'OPEN'"
    print sql
    return sql

def load_json(list_res):
    db = connect_db()
    cursor = db.cursor()
    res = []
    for tup in list_res:
        try:
            dict = {"type": tup[0], "no": tup[1], "title": tup[2], "description": tup[3], "payment": tup[4],
                    "opentime": tup[5]}
            if tup[0] == 'SURVEY':
                sql = "SELECT MINAGE,MAXAGE,GENDER_RESTRICT,SURVEY_RESTRICT FROM SURVEY WHERE SNO= %d" % tup[1]
                cursor.execute(sql)
                l = cursor.fetchall()
                dict["min_age"] = l[0][0]
                dict["max_age"] = l[0][1]
                dict["gender_restrict"] = l[0][2]
                dict["survey_restrict"] = l[0][3]
                sql = "SELECT WHAT FROM SURVEY_SUBJECT WHERE SNO = %d" % tup[1]
                cursor.execute(sql)
                l = cursor.fetchall()
                dict["subject1"] = l[0][0] if len(l) >= 1 else ""
                dict["subject2"] = l[1][0] if len(l) >= 2 else ""
                dict["subject3"] = l[2][0] if len(l) >= 3 else ""
            else:
                sql = "SELECT DATATYPE FROM TASK_WITH_FILE, FILE WHERE TASK_WITH_FILE.FNO=FILE.FNO AND TNO =%d" % tup[1]
                cursor.execute(sql)
                l = cursor.fetchall()
                dict["datatype"] = l[0][0]
            res.append(dict)
        except Exception:
            print 'error at sql_list'
            pass

    db.commit()
    db.close()

    return res


def get_list_from_db(subject=None, datatype=None, type=None,order=None, user='root', pwd='123456'):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'ScholarDB' AND table_name = 'LIST' ")
    l = cursor.fetchall();
    print l
    if(l[0][0]==1):
        cursor.execute("DROP VIEW LIST")

    sql = "CREATE VIEW LIST (NO, TYPE, TITLE, DESCRIPTION, PAYMENT, OPENTIME) AS "

    if type == 'SURVEY':
        sql += add_survey_to_list(subject,user,pwd)

    if type == 'TASK':
        sql += add_task_to_list(datatype,user,pwd)

    if type == "BOTH":
        sql += add_survey_to_list(subject,user,pwd) + " UNION " + add_task_to_list(datatype,user,pwd)

    print sql

    cursor.execute(sql)

    sql = "SELECT TYPE,NO,TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM LIST ORDER BY " + order
    cursor.execute(sql)

    list_res = cursor.fetchall()

    print list_res

    res = load_json(list_res)

    db.commit()
    db.close()

    return res


def search(subject=None, datatype=None, type=None, pattern=None, order=None, isDesc=None, user='root', pwd=123456):
    db = connect_db()
    cursor = db.cursor()

    get_list_from_db(subject, datatype, type, order, user, pwd)

    sql = "SELECT TYPE,NO,TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM LIST WHERE TITLE LIKE '%" + pattern + "%'"

    print "isDesc:",isDesc

    if isDesc == '1':
        sql += "OR DESCRIPTION LIKE '%" + pattern + "%'"

    sql += "ORDER BY " + order

    print sql

    cursor.execute(sql)

    list_res = cursor.fetchall()
    res = load_json(list_res)

    db.commit()
    db.close()

    return res

