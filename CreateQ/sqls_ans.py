from sqls import SurveyQuestions
from common_file import *
import time
import copy

class SurveyAnswer:
    def __init__(self):
        self.answer_list = []
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
        for ans in self.answer_list:
            sql = "INSERT INTO ANSWER(UNO,QNO,VALUE) VALUES (%d,%d,'%s')" % \
                  (ans.uno,ans.qno,ans.value)
            cursor.execute(sql)
            sql = "INSERT INTO PARTICIPATION(UNO,SNO,SUBMIT_TIME,TIME_CONSUMED) VALUES(%d,%d,'%s',%d)" % \
                  (ans.uno,self.sno,self.submit_time,self.consumed_time)
            cursor.execute(sql)
        db.commit()


