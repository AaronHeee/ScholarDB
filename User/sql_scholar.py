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
        self.money = ""
        self.mail = ""
    def to_json(self):
        json = {'uno':self.uno,'uname':self.uname,'inst':self.inst,'nation':self.nation,'city':self.city,'money':self.money,
                'mail':self.mail}
        return json
    def load_basic_info_from_db(self,uno):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT USERINFO.UNO,UNAME,INST,NATION,CITY,MONEY,MAIL FROM SCHOLAR,USERINFO WHERE SCHOLAR.UNO = USERINFO.UNO "
                       "AND USERINFO.UNO = %d" % uno)
        self.uno,self.uname,self.inst,self.nation,self.city,self.money,self.mail = cursor.fetchone()[0:7]
        db.close()

def project_list_of_scholar(uno):
    json = get_scholar_list_from_db(uno = uno,subject = [],type='BOTH',order = 'OPENTIME DESC')
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




