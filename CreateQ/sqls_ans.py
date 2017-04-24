# encoding=utf-8
from sqls import SurveyQuestions
from common_file import *
import time
import copy
from collections import OrderedDict

def tup_to_dict(key_list,res_tup):
    xref = {}
    for i,key in enumerate(key_list):
        xref[key] = res_tup[i]
    return xref

class SurveyAnswer:
    def __init__(self):
        self.answer_list = []
        self.qa_dict= {}
        self.consumed_time = 0
        self.status = ""
        self.submit_time = -1
        self.sno = -1
    class Answer:
        def __init__(self):
            self.uno = -1
            self.qno = -1
            self.value = ""
            self.type = ""
    def parse(self,json_query,uno = -1,server_time = 0): #multiple choice question answer is stored seperately
        json = dict(json_query)
        self.uno = int(uno)
        self.submit_time = server_time
        self.status = "pending"
        self.sno = int(json['sno'][0])
        self.consumed_time = int(json['time_consumed'][0])
        i = 0
        while 'res[%d][qno]' % i in json.keys():
            t = SurveyAnswer.Answer()
            t.uno = int(uno)
            t.qno = int(json['res[%d][qno]' % i][0])
            t.type = json['res[%d][type]' % i][0]
            if t.type == 'qa':
                t.value = json['res[%d][value]' % i][0]
                self.answer_list.append(t)
            else:
                for v in json['res[%d][value][]' % i]:
                    t.value = v
                    self.answer_list.append(copy.deepcopy(t))
            print self.answer_list
            i += 1

    def add_to_db(self):
        db = connect_db()
        cursor = db.cursor()
        uno_hist = []
        for ans in self.answer_list:
            sql = "INSERT INTO ANSWER(UNO,QNO,VALUE) VALUES (%d,%d,'%s')" % \
                  (ans.uno,ans.qno,ans.value)
            cursor.execute(sql)
            if ans.uno not in uno_hist:
                sql = "INSERT INTO PARTICIPATION(UNO,SNO,SUBMIT_TIME,TIME_CONSUMED,STATUS) VALUES(%d,%d,'%s',%d,'%s')" % \
                      (ans.uno, self.sno, self.submit_time, self.consumed_time,self.status)
                cursor.execute(sql)
                uno_hist.append(ans.uno)
        db.commit()

    def to_json_list_by_user(self,sno):
        json_list = []
        db = connect_db()
        cursor = db.cursor()
        #参与调研的人
        #需要的隐私到时候给予显示
        sql = "SELECT DISTINCT USERINFO.UNO,UNAME,GENDER,AGE,NATION,CITY FROM USERINFO,PARTICIPATION WHERE SNO = %d AND USERINFO.UNO = PARTICIPATION.UNO" % sno
        cursor.execute(sql)
        users = cursor.fetchall()
        cursor.execute("SELECT WHAT FROM PRIVACY WHERE SNO = %d" % sno)
        privacy = cursor.fetchall()
        #Q.A. --> JSON
        for tup in users:
            json = {}
            json['qa'] = OrderedDict()
            uno = tup[0]
            sql = "SELECT TITLE,VALUE FROM QUESTION,ANSWER WHERE QUESTION.QNO = ANSWER.QNO AND UNO = %d AND SNO = %d" % (uno,sno)
            cursor.execute(sql)
            qas = cursor.fetchall()
            sql = "SELECT SNO,SUBMIT_TIME,TIME_CONSUMED,STATUS FROM PARTICIPATION WHERE PARTICIPATION.UNO = %d AND SNO = %d" %(uno,sno)
            cursor.execute(sql)
            info = cursor.fetchall()
            if info[0][3] == 'DELETED':
                continue
            for qa in qas:
                if qa[0] in json['qa'].keys():
                    json['qa'][qa[0]] += ';'+qa[1]
                else:
                    json['qa'][qa[0]] = qa[1]
            json['submit_time'] = info[0][1]
            json['time_consumed'] = info[0][2]
            user_info_dict = tup_to_dict(['UNO', 'UNAME', 'GENDER', 'AGE', 'NATION', 'CITY'], tup)
            #mask privacies
            available_privacy = [translation_dict[i[0]] for i in privacy if i[0] in translation_dict.keys()]
            for key in user_info_dict.keys():
                if key not in available_privacy:
                    user_info_dict.pop(key)
            json['privacy'] = dict(zip([translation_dict_r[i] for i in user_info_dict.keys()],[translation_dict_r[i] for i in user_info_dict.values()]))
            json['uno'] = uno
            json_list.append(json)


        return json_list

def check_authorization(uno,sno,access_list):
    db = connect_db()
    cursor = db.cursor()
    for access in access_list:
        cursor.execute("SELECT * FROM SCHOLAR_OWN_SURVEY WHERE ACCESS = '%s' AND UNO = %d AND SNO = %d" % (access,uno,sno))
        if cursor.fetchone:
            return True
    return False

def load_contributor(sno):
    json = {'contributor':[],'contributor_cnt':0}
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT USERINFO.UNO,UNAME,INST FROM USERINFO,SCHOLAR,SCHOLAR_OWN_SURVEY WHERE USERINFO.UNO = SCHOLAR.UNO AND USERINFO.UNO = SCHOLAR_OWN_SURVEY.UNO AND SNO = %d" % sno)
    # Cooperator --> JSON
    tups = cursor.fetchall()
    for tup in tups:
        tjson = {'uno':tup[0],'uname':tup[1],'inst':tup[2]}
        json['contributor'].append(tjson)
        json['contributor_cnt'] += 1
    db.close()
    return json

def load_summary_management(sno):
    json = {'answer_cnt':0,'stage':''}
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(DISTINCT UNO) FROM PARTICIPATION WHERE SNO = %d" % sno)
    json['answer_cnt'] = cursor.fetchone()[0]
    cursor.execute("SELECT STAGE FROM SURVEY WHERE SNO = %d" % sno)
    json['stage'] = cursor.fetchone()[0]
    db.close()
    return json

def delete_answer(uno,sno):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM ANSWER WHERE UNO = %d AND QNO IN (SELECT QNO FROM QUESTION WHERE SNO = %d)" % (uno,sno))
    cursor.execute("UPDATE PARTICIPATION SET STATUS = 'DELETED' WHERE UNO = %d AND SNO = %d" % (uno,sno))
    db.commit()
    db.close()

def search_scholar_by_name(name):
    db = connect_db()
    user_list = []
    cursor = db.cursor()
    cursor.execute("SELECT SCHOLAR.UNO,INST FROM SCHOLAR,USERINFO WHERE UNAME = '%s'" % name)
    users = cursor.fetchall()
    for tup in users:
        tdict = {'uno':tup[0],'inst':tup[1]}
        user_list.append(tdict)
    db.close()
    return user_list