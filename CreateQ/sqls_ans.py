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

def override_sql(sql,override = True):
    if not override:
        return sql
    sql = sql.replace('SNO','TNO')
    sql = sql.replace('PARTICIPATION','PARTICIPATION_TASK')
    sql = sql.replace('SURVEY','TASK')
    return sql

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

    #update 0427 更好的接口：答案可以通过字符串或者链表形式加入到json
    def to_json_list_by_user(self,sno,concat_mode = "strconcat"):
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
            #答案通过“字符串连接”向服务器发送,这样一来,任何类型的答案都是一个字符串（包括多选题）,但是不利于JS分析
            if concat_mode == 'strconcat':
                for qa in qas:
                    if qa[0] in json['qa'].keys():
                        json['qa'][qa[0]] += ';'+qa[1]
                    else:
                        json['qa'][qa[0]] = qa[1]
            #答案通过“链表”向服务器发送,这样一来,任何类型德答案都是一个list,再js端就是Array,除了多选题长度都是1.
            else:
                for qa  in qas:
                    if qa[0] in json['qa'].keys():
                        json['qa'][qa[0]].append(qa[1])
                    else:
                        json['qa'][qa[0]].list = [qa[1]]
            json['submit_time'] = info[0][1]
            json['time_consumed'] = info[0][2]
            user_info_dict = tup_to_dict(['UNO', 'UNAME', 'GENDER', 'AGE', 'NATION', 'CITY'], tup)
            #mask privacies
            available_privacy = [translation_dict[i[0]] for i in privacy if i[0] in translation_dict.keys()]
            for key in user_info_dict.keys():
                if key not in available_privacy:
                    user_info_dict.pop(key)
            json['privacy'] = dict(zip([translation_dict_r[i] for i in user_info_dict.keys()],[i for i in user_info_dict.values()]))
            json['uno'] = uno
            json_list.append(json)

        return json_list

def check_authorization(uno,sno,access_list,override_task = False):
    db = connect_db()
    cursor = db.cursor()
    for access in access_list:
        sql = "SELECT * FROM SCHOLAR_OWN_SURVEY WHERE ACCESS = '%s' AND UNO = %d AND SNO = %d" % (access, uno, sno)
        if override_task:
            sql = override_sql(sql)
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:
            return True
    return False

def load_contributor(sno,override_task = False):
    json = {'contributor':[],'contributor_cnt':0}
    db = connect_db()
    cursor = db.cursor()
    sql = "SELECT USERINFO.UNO,UNAME,INST,ACCESS FROM USERINFO,SCHOLAR,SCHOLAR_OWN_SURVEY WHERE USERINFO.UNO = SCHOLAR.UNO" \
          " AND USERINFO.UNO = SCHOLAR_OWN_SURVEY.UNO AND SNO = %d" % sno
    if override_task:
        sql = override_sql(sql)
    cursor.execute(sql)
    # Cooperator --> JSON
    tups = cursor.fetchall()
    for tup in tups:
        tjson = {'uno':tup[0],'uname':tup[1],'inst':tup[2],'access':tup[3]}
        json['contributor'].append(tjson)
        json['contributor_cnt'] += 1
    db.close()
    return json

def load_summary_management(sno,override_task = False):
    json = {'answer_cnt':0,'stage':''}
    db = connect_db()
    cursor = db.cursor()
    sql = "SELECT COUNT(DISTINCT UNO) FROM PARTICIPATION WHERE SNO = %d AND STATUS != 'DELETED'" % sno
    if override_task:
        sql = override_sql(sql)
    cursor.execute(sql)
    json['answer_cnt'] = cursor.fetchone()[0]
    sql = "SELECT STAGE FROM SURVEY WHERE SNO = %d" % sno
    if override_task:
        sql = override_sql(sql)
    cursor.execute(sql)
    json['stage'] = cursor.fetchone()[0]
    sql = "SELECT PUBLICITY FROM PUBLICITY_SURVEY WHERE SNO = %d" % sno
    if override_task:
        sql = override_sql(sql)
    cursor.execute(sql)
    t_publicity = cursor.fetchone()
    if t_publicity:
        json['publicity'] = translation_dict_r[t_publicity[0]]
    else:
        json['publicity'] = "未设置"
    sql ="SELECT TITLE,DESCRIPTION,OPENTIME FROM SURVEY WHERE SNO = %d" % sno
    if override_task:
        sql = override_sql(sql)
    cursor.execute(sql)
    res = cursor.fetchone()
    json['title'],json['description'],json['opentime'] = res[0],res[1],res[2]
    db.close()
    return json

def delete_answer(uno,sno,override_task = False):
    db = connect_db()
    cursor = db.cursor()
    if not override_task:
        cursor.execute("DELETE FROM ANSWER WHERE UNO = %d AND QNO IN (SELECT QNO FROM QUESTION WHERE SNO = %d)" % (uno,sno))
    cursor.execute(override_sql("UPDATE PARTICIPATION SET STATUS = 'DELETED' WHERE UNO = %d AND SNO = %d" % (uno,sno),override_task))
    db.commit()
    db.close()

def add_contributor(uno,sno,override_task = False):
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO SCHOLAR_OWN_SURVEY(SNO,UNO,ACCESS) VALUES(%d,%d,'%s')" % (sno,uno,'COOPERATOR')
    if override_task:
        sql = override_sql(sql)
    cursor.execute(sql)
    db.commit()
    db.close()

def close_project(sno,publicity,override_task = False):
    db = connect_db()
    cursor = db.cursor()
    sql ="SELECT * FROM PUBLICITY_SURVEY WHERE SNO = %d" % sno
    if override_task:
        sql = override_sql(sql)
    cursor.execute(sql)
    if cursor.fetchone():
        cursor.execute(override_sql("UPDATE PUBLICITY_SURVEY SET PUBLICITY = '%s' WHERE SNO = %d" % (publicity, sno),override_task))
    else:
        cursor.execute(override_sql("INSERT INTO PUBLICITY_SURVEY(SNO,PUBLICITY) VALUES(%d,'%s')"% (sno,publicity),override_task))
    cursor.execute(override_sql("UPDATE SURVEY SET STAGE = 'CLOSED' WHERE SNO = %d" % sno,override_task))
    cursor.execute(override_sql("UPDATE PARTICIPATION SET STATUS = 'adopted' WHERE STATUS = 'pending' and SNO = %d" % sno,override_task))
    db.commit()
    db.close()

def delete_project(sno,override_task = False):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM CHOICE WHERE QNO IN (SELECT QNO FROM QUESTION WHERE SNO = %d)" % sno)
    cursor.execute("DELETE FROM QUESTION WHERE SNO = %d" % sno)
    cursor.execute("DELETE FROM SCHOLAR_OWN_SURVEY WHERE SNO = %d" % sno)
    cursor.execute("DELETE FROM PUBLICITY_SURVEY WHERE SNO = %d" % sno)
    cursor.execute("DELETE FROM PRIVACY WHERE SNO = %d" % sno)
    cursor.execute("DELETE FROM SURVEY_SUBJECT WHERE SNO = %d" % sno)
    cursor.execute("UPDATE PARTICIPATION SET STATUS = 'survey_deleted' WHERE sno = %d" % sno)
    cursor.execute("DELETE FROM SURVEY WHERE SNO = %d" % sno)
    db.commit()
    db.close()

def load_date_number(sno,override_task = False):
    db = connect_db()
    cursor = db.cursor()
    sql = "SELECT DATE_FORMAT(SUBMIT_TIME,'%%Y-%%m-%%d'),COUNT(SNO) FROM PARTICIPATION" \
          " WHERE SNO=%d GROUP BY DATE_FORMAT(SUBMIT_TIME,'%%Y-%%m-%%d')"% sno
    if override_task:
        sql = override_sql(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    date = []
    number = []
    json = {}
    for i in res:
        date.append(i[0])
        number.append(i[1])
    json["date"] = date
    json["number"] = number
    print json
    db.close()
    return json

def load_gender(sno,override_task = False):
    db = connect_db()
    cursor = db.cursor()
    json = {}
    sql = "SELECT COUNT(*) FROM PARTICIPATION P,USERINFO U WHERE SNO=%d AND P.UNO=U.UNO AND GENDER='Female'" % sno
    if override_task:
        sql = override_sql(sql)
    cursor.execute(sql)
    json['Female']=cursor.fetchall()[0][0]
    sql = "SELECT COUNT(*) FROM PARTICIPATION P,USERINFO U WHERE SNO=%d AND P.UNO=U.UNO AND GENDER='Male'" % sno
    if override_task:
        sql = override_sql(sql)
    cursor.execute(sql)
    json['Male'] = cursor.fetchall()[0][0]
    db.close()
    return  json

def load_location(sno,override_task = False):
    db = connect_db()
    cursor = db.cursor()
    json = []

    sql = "SELECT CITY, COUNT(*) FROM PARTICIPATION P,USERINFO U WHERE SNO=%d AND P.UNO=U.UNO GROUP BY CITY" % sno
    if override_task:
        sql = override_sql(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    for i in res:
        city = {}
        city['name'] = i[0]
        city['value'] = i[1]
        json.append(city)
    print "location:",json
    db.close()
    return json

def to_json_list_by_user_task(tno,concat_mode = 'strconcat'):
    json_list = []
    db = connect_db()
    cursor = db.cursor()
    sql = "SELECT DISTINCT UNO,SUBMIT_TIME FROM PARTICIPATION_TASK WHERE TNO = %d" % tno
    cursor.execute(sql)
    users = cursor.fetchall()
    for tup in users:
        json = {'uno':tup[0],'submit_time':tup[1]}
        uno = tup[0]
        sql = "SELECT FSNO FROM FILE_SLICE WHERE TNO = %d AND UNO = %d" % (tno,uno)
        cursor.execute(sql)
        fsno_set = cursor.fetchall()
        for tup2 in fsno_set:
            if concat_mode == 'strconcat':
                if 'fsno' not in json.keys():
                    json['fsno'] = '第'+str(tup2[0])+'组'
                else:
                    json['fsno'] +='，第'+str(tup2[0])+'组'
            else:
                if 'fsno' not in json.keys():
                    json['fsno'] = [tup2[0]]
                else:
                    json['fsno'].append(tup2[0])
        json_list.append(json)
    return json_list


