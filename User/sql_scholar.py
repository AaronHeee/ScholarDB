# encoding=utf-8
from common_file import *
from CreateQ.sqls import *
from CreateQ.sqls_scholar_list import get_scholar_list_from_db
class Scholar:
    def __init__(self):
        self.uno = -1
        self.uname = ""
        self.inst = ""
        self.nation = ""
        self.city = ""
        self.money = 0
        self.mail = ""
        self.age = 0
        self.gender = ""
    def to_json(self,restrict =False):
        if restrict:
            return {'uno':self.uno,'uname':self.uname,'inst':self.inst,'usertype':'Scholar','mail':self.mail}
        json = {'uno':self.uno,'uname':self.uname,'inst':self.inst,'nation':self.nation,'city':self.city,'money':self.money,
                'mail':self.mail,'age':self.age,'gender':self.gender,'usertype':'Scholar'}
        return json
    def load_basic_info_from_db(self,uno):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT USERINFO.UNO,UNAME,INST,NATION,CITY,MONEY,MAIL,AGE,GENDER FROM SCHOLAR,USERINFO WHERE SCHOLAR.UNO = USERINFO.UNO "
                       "AND USERINFO.UNO = %d" % uno)
        res = cursor.fetchone()
        print res
        self.uno,self.uname,self.inst,self.nation,self.city,self.money,self.mail,self.age,self.gender = res[0:9]
        db.close()

class Volunteer:
    def __init__(self):
        self.uno = -1
        self.uname = ""
        self.nation = ""
        self.city = ""
        self.cred = 0
        self.mail = ""
        self.money = 0
        self.age = 0
        self.gender = ""
    def to_json(self,restrict =False):
        if restrict:
            return {'uno':self.uno,'uname':self.uname,'cred':self.cred,'usertype':'Volunteer','mail':self.mail}
        json = {'uno': self.uno, 'uname': self.uname, 'cred': self.cred, 'nation': self.nation, 'city': self.city,
                'money': self.money,'mail': self.mail, 'age': self.age, 'gender': self.gender,'usertype':'Volunteer'}
        return json
    def load_basic_info_from_db(self,uno):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT USERINFO.UNO,UNAME,CRED,NATION,CITY,MONEY,MAIL,AGE,GENDER FROM VOLUNTEER,USERINFO WHERE VOLUNTEER.UNO = USERINFO.UNO "
                       "AND USERINFO.UNO = %d" % uno)
        self.uno,self.uname,self.cred,self.nation,self.city,self.money,self.mail,self.age,self.gender = cursor.fetchone()[0:9]
        db.close()

def get_user_type(uno):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT USERTYPE FROM USERINFO WHERE UNO = %d" % uno)
    try:
        usertype = cursor.fetchone()[0]
    except TypeError:
        db.close()
        return None
    db.close()
    return usertype

def project_list_of_scholar(uno):
    json = get_scholar_list_from_db(uno = uno,subject = [],type='BOTH',order = 'OPENTIME DESC',onlyforme=True)
    print json
    return json

def participation_list(uno):
    db = connect_db()
    cursor = db.cursor()
    json = []
    cursor.execute("SELECT PARTICIPATION.SNO,TITLE,SUBMIT_TIME,PAYMENT,STATUS FROM PARTICIPATION,SURVEY WHERE UNO = %d AND SURVEY.SNO = PARTICIPATION.SNO" % uno)
    tups = cursor.fetchall()
    cursor.execute("SELECT PARTICIPATION_TASK.TNO,TITLE,SUBMIT_TIME,PAYMENT,STATUS FROM PARTICIPATION_TASK,TASK WHERE UNO = %d AND TASK.TNO = PARTICIPATION_TASK.TNO" % uno)
    tups2 = cursor.fetchall()
    for tup in tups:
        tjson = {'NO':tup[0],'TITLE':tup[1],'SUBMIT_TIME':tup[2],'TYPE':'SURVEY','PAYMENT':tup[3],'STATUS':translation_dict_r[tup[4]]}
        json.append(tjson)
    for tup in tups2:
        tjson = {'NO':tup[0],'TITLE':tup[1],'SUBMIT_TIME':tup[2],'TYPE':'TASK','PAYMENT':tup[3],'STATUS':translation_dict_r[tup[4]]}
        json.append(tjson)
    return json #list

def search_scholar_by_name(name,also_by_id = True):
    db = connect_db()
    user_list = []
    cursor = db.cursor()
    sql = "SELECT SCHOLAR.UNO,UNAME,INST FROM SCHOLAR,USERINFO WHERE SCHOLAR.UNO = USERINFO.UNO AND UNAME = '%s'" % name
    if also_by_id:
        sql += " OR SCHOLAR.UNO = USERINFO.UNO AND SCHOLAR.UNO = '%s'" % name
    cursor.execute(sql)
    users = cursor.fetchall()
    for tup in users:
        tdict = {'uno':tup[0],'uname':tup[1],'inst':tup[2]}
        user_list.append(tdict)
    db.close()
    return user_list



