#encoding=utf-8

import MySQLdb
import time
from common_file import connect_db

def add_survey_to_scholar_list(uno=None, subject=None, user='root', pwd='dbpjdbpj',onlyforme = True,publicity = 'BOTH'): #onlyforme为false时,uno限制被去除

    sql = "SELECT SNO, TYPE, TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM SURVEY WHERE "
    condition = []
    if subject != [None] and subject != [''] and subject != []:
        for sub in subject:
            if sub == '' or sub == ' ':
                continue
            condition.append(" SNO IN (SELECT SNO FROM SURVEY_SUBJECT WHERE WHAT = '%s')" % sub)
    if condition != None and condition != []:
        sql += ' AND '.join(condition)
        sql += ' AND'
    if publicity == "PUBLIC" or publicity == "PRIVATE":
        sql += 'AND SNO IN (SELECT SNO FROM PARTICIPATION_SURVET WHERE SURVEY.SNO = PUBLICITY_SURVEY.SNO AND  PUBLICITY = %s ) AND' % publicity

    if onlyforme:
        sql += " SNO IN (SELECT SNO FROM SCHOLAR_OWN_SURVEY WHERE UNO = %d)" % uno
    else:
        sql += " true"
    print sql

    return sql

def add_task_to_scholar_list(uno=None, datatype=None, user='root', pwd='dbpjdbpj',onlyforme = True,publicity = 'BOTH'):

    sql = "SELECT TASK.TNO,TYPE,TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM TASK "
    if datatype != '' and datatype != None:
        sql += ",FILE WHERE FILE.DATATYPE='%s' AND" % datatype

    else:
        sql += " WHERE"

    if publicity == "PUBLIC" or publicity == "PRIVATE":
        sql += ' TASK.TNO IN (SELECT TNO FROM PARTICIPATION_TASK WHERE TASK.TNO = PUBLICITY_TASK.TNO AND PUBLICITY = %s AND' % publicity

    if onlyforme:
        sql += " TNO IN (SELECT TNO FROM SCHOLAR_OWN_TASK WHERE UNO = %d)" %uno
    else:
        sql += " true"


    return sql

def load_json(list_res):
    db = connect_db()
    cursor = db.cursor()
    res = []
    for tup in list_res:
        dict = {"type": tup[0], "no": tup[1], "title": tup[2], "description": tup[3], "payment": tup[4], "opentime": tup[5]}
        if tup[0] == 'SURVEY':
            sql = "SELECT MINAGE,MAXAGE,GENDER_RESTRICT,SURVEY_RESTRICT FROM SURVEY WHERE SNO= %d" % tup[1]
            cursor.execute(sql)
            l = cursor.fetchall()
            dict["min_age"] = l[0][0]
            dict["max_age"] = l[0][1]
            dict["gender_restrict"] = l[0][2]
            dict["survey_restrict"] = l[0][3]
            #added by AuCson 0428: PUBLICITY:
            sql = "SELECT PUBLICITY FROM PUBLICITY_SURVEY WHERE SNO = %d" % tup[1]
            cursor.execute(sql)
            try:
                dict["publicity"] = cursor.fetchone()[0]
            except TypeError:
                dict['publicity'] =  ''
            #end add
            sql = "SELECT WHAT FROM SURVEY_SUBJECT WHERE SNO = %d" % tup[1]
            cursor.execute(sql)
            l = cursor.fetchall()
            print l
            dict["subject1"] = l[0][0] if len(l) >= 1 else ""
            dict["subject2"] = l[1][0] if len(l) >= 2 else ""
            dict["subject3"] = l[2][0] if len(l) >= 3 else ""
        else:
            #added by Aucson 0428
            sql = "SELECT PUBLICITY FROM PUBLICITY_TASK WHERE TNO = %d" % tup[1]
            cursor.execute(sql)
            try:
                dict["publicity"] = cursor.fetchone()[0]
            except TypeError:
                dict['publicity'] =  ''
            #end add
            sql = "SELECT DATATYPE,SUM(SEND),SUM(RECEIVE),COUNT(FSNO) FROM FILE F,FILE_SLICE S WHERE TNO =%d AND F.FNO=S.FNO GROUP BY F.FNO" % tup[1]
            print sql
            cursor.execute(sql)
            l = cursor.fetchall()

            if l:
                dict["datatype"] = l[0][0]
                dict["num"] = l[0][1]
                dict["now"] = l[0][2]
                dict["slice"] = l[0][3]
        res.append(dict)

    db.commit()
    db.close()

    return res


def get_scholar_list_from_db(uno=None, subject=None, datatype=None,publicity=None,type=None,order=None, user='root', pwd='123456',onlyforme = True):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'ScholarDB' AND table_name = 'LIST' ")
    l = cursor.fetchall();
    print l
    if(l[0][0]==1):
        cursor.execute("DROP VIEW LIST")

    sql = """CREATE VIEW LIST (NO, TYPE, TITLE, DESCRIPTION, PAYMENT, OPENTIME)
            AS
            """

    if type == 'SURVEY':
        sql += add_survey_to_scholar_list(uno,subject,user,pwd,onlyforme,publicity)

    if type == 'TASK':
        sql += add_task_to_scholar_list(uno,datatype,user,pwd,onlyforme,publicity)

    if type == "BOTH":
        sql += add_survey_to_scholar_list(uno,subject,user,pwd,onlyforme,publicity) + " UNION " + add_task_to_scholar_list(uno,datatype,user,pwd,onlyforme,publicity)

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


def search(uno=None, subject=None, datatype=None, type=None, pattern=None, order=None, isDesc=None, user='root', pwd=123456):
    db = connect_db()
    cursor = db.cursor()

    get_scholar_list_from_db(uno, subject, datatype, type, order, user, pwd)

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

