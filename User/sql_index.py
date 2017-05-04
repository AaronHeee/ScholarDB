# coding=utf-8
# encoding=utf-8
from common_file import *

def get_statistics():
    db = connect_db()
    cursor = db.cursor()
    json = {}
    cursor.execute("SELECT COUNT(UNO) FROM USERINFO WHERE USERTYPE = 'Scholar'")
    json['scholar_cnt'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(UNO) FROM USERINFO WHERE USERTYPE = 'Volunteer'")
    json['volunteer_cnt'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(SNO) FROM SURVEY WHERE STAGE = 'OPEN'")
    json['open_cnt'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(TNO) FROM TASK WHERE STAGE = 'OPEN'")
    json['open_cnt'] += cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(SNO) FROM PUBLICITY_SURVEY WHERE PUBLICITY = 'PUBLIC'")
    json['public_cnt'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(TNO) FROM PUBLICITY_TASK WHERE PUBLICITY = 'PUBLIC'")
    json['public_cnt'] += cursor.fetchone()[0]
    db.close()
    return json

def get_public_survey(min,max): #一次显示第Min到第max个
    db = connect_db()
    cursor = db.cursor()
    json_list = []
    sql= "SELECT SURVEY.SNO,USERINFO.UNO,UNAME,INST,TITLE,OPENTIME FROM USERINFO,SCHOLAR,SCHOLAR_OWN_SURVEY,SURVEY,PUBLICITY_SURVEY"\
                   " WHERE USERINFO.UNO = SCHOLAR.UNO AND SCHOLAR.UNO = SCHOLAR_OWN_SURVEY.UNO AND SCHOLAR_OWN_SURVEY.SNO = SURVEY.SNO"\
                   " AND SURVEY.SNO = PUBLICITY_SURVEY.SNO AND PUBLICITY = 'PUBLIC' AND ACCESS = 'OWNER' ORDER BY OPENTIME DESC"

    print sql
    cursor.execute(sql)
    tups = cursor.fetchall()
    for tup in tups:
        json = {'SNO':tup[0],'UNO':tup[1],'UNAME':tup[2],'INST':tup[3],'TITLE':tup[4],'DESCRIPTION':tup[5],'OPENTIME':tup[5]}
        json_list.append(json)
    return json_list[min:max]

def get_public_task(min,max): #一次显示第Min到第max个
    db = connect_db()
    cursor = db.cursor()
    json_list = []
    sql= "SELECT TASK.TNO,USERINFO.UNO,UNAME,INST,TITLE,OPENTIME FROM USERINFO,SCHOLAR,SCHOLAR_OWN_TASK,TASK,PUBLICITY_TASK"\
                   " WHERE USERINFO.UNO = SCHOLAR.UNO AND SCHOLAR.UNO = SCHOLAR_OWN_TASK.UNO AND SCHOLAR_OWN_TASK.TNO = TASK.TNO"\
                   " AND TASK.TNO = PUBLICITY_TASK.TNO AND PUBLICITY = 'PUBLIC' AND ACCESS = 'OWNER' ORDER BY OPENTIME DESC"
    print sql
    cursor.execute(sql)
    tups = cursor.fetchall()
    for tup in tups:
        json = {'TNO':tup[0],'UNO':tup[1],'UNAME':tup[2],'INST':tup[3],'TITLE':tup[4],'OPENTIME':tup[5]}
        json_list.append(json)
    return json_list[min:max]