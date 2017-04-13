#encoding=utf-8
import MySQLdb
import time
from common_file import connect_db
class SurveyTitle:
    def __init__(self):
        self.description = ''
        self.title = ''
        self.subject = []
    def parse(self,post):
        self.title = post['JSON1[title]']
        self.description = post['JSON1[description]']
        self.subject = post['JSON1[subject]'][:-1].split(',')

class SurveyDetail:
    def __init__(self):
        self.min_age = 0
        self.max_age = 200
        self.gender_restrict = 'any'
        self.survey_restrict = 'any'
        self.privacy = []
        self.payment = 0
        self.owner = ''
        self.opentime = ''
        #多值属性！
    def parse(self,post,owner,time):
        try:
            self.min_age = max(int(post['JSON2[min-age]']),0)
            self.max_age = min(int(post['JSON2[max-age]']),200)
        except ValueError:
            pass
        self.gender_restrict = post['JSON2[gender-restrict]']
        self.survey_restrict = post['JSON2[survey-restrict]']
        self.privacy = post['JSON2[privacy]'][:-1].split(',')
        self.payment = min(0,int(post['JSON2[payment]']))
        self.owner = owner
        self.opentime = time

class SurveyQuestions:
    def __init__(self):
        self.question_list = []
    class Question:
        def __init__(self):
            self.type = ""
            self.title = ""
            self.supplement = ""
            self.supplement_type = ""
            #QA:text,number QSC:single.multiple
            self.input_type = ""
            self.choice = []
    def parse(self,post):
        i = 1
        while 'JSON3[%d][title]'%i in post.keys():
            q= SurveyQuestions.Question()
            q.title = post['JSON3[%d][title]'%i]
            q.type = post['JSON3[%d][type]'%i]
            q.supplement = post['JSON3[%d][supplement]' % i]
            q.supplement_type = post['JSON3[%d][suptype]'%i]
            q.input_type = post['JSON3[%d][inputtype]'%i]
            if q.type == 'qsc':
                q.choice = post['JSON3[%d][choice]'%i][:-1].split(',')
            self.question_list.append(q)
            i += 1
        print self.question_list

def add_survey_to_db(title,detail,questions):
    db = connect_db()
    cursor = db.cursor()
    #title

    sql = "INSERT INTO SURVEY(SNO,TITLE,DESCRIPTION,MINAGE,MAXAGE,GENDER_RESTRICT,SURVEY_RESTRICT,PAYMENT,STAGE,OPENTIME) VALUES" \
          "(NULL,'%s','%s',%d,%d,'%s','%s',%d,'OPEN','%s')" % (title.title,title.description,detail.min_age,detail.max_age,
                                                detail.gender_restrict,detail.survey_restrict,detail.payment,detail.opentime)
    cursor.execute(sql)
    cursor.execute("SELECT MAX(SNO) FROM SURVEY")
    sno = cursor.fetchall()[0][0]

    cursor.execute("SELECT UNO FROM USERINFO WHERE UNAME = '%s'" % detail.owner)
    uno = cursor.fetchall()[0][0]

    sql = "INSERT INTO SCHOLAR_OWN_SURVEY(UNO,SNO,ACCESS) VALUES(%d,%d,'owner')" % (uno,sno)
    cursor.execute(sql)

    for subject in title.subject:
        sql = "INSERT INTO SURVEY_SUBJECT(SNO,WHAT) VALUES(%d,'%s')" % (sno,subject)
        cursor.execute(sql)
    for privacy in detail.privacy:
        sql = "INSERT INTO PRIVACY(SNO,WHAT) VALUES (%d,'%s')" % (sno,privacy)
        cursor.execute(sql)
    for question in questions.question_list:
        sql = "INSERT INTO QUESTION(QNO,SNO,TITLE,SUPPLEMENT,SUPPLEMENT_TYPE,TYPE,INPUTTYPE) VALUES" \
              "(NULL,%d,'%s','%s','%s','%s','%s')" % (sno,question.title,question.supplement,question.supplement_type,
                                                    question.type,question.input_type)
        cursor.execute(sql)
        if question.type == 'qsc':
            cursor.execute("SELECT MAX(QNO) FROM QUESTION")
            qno = cursor.fetchall()[0][0]
            for i,choice in enumerate(question.choice):
                sql = "INSERT INTO CHOICE(CNO,PLACE,QNO,CONTENT) VALUES(NULL,%d,%d,'%s')" % (i,qno,choice)
                cursor.execute(sql)
    db.commit()




