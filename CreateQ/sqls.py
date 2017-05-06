#encoding=utf-8
import MySQLdb
import time

#Created by auson
from common_file import connect_db


class SurveyTitle:
    def __init__(self):
        self.description = ''
        self.title = ''
        self.subject = []
        self.opentime = ''
        self.payment = 0
        self.publicity = ''
    def parse(self, post):
        self.title = post['JSON1[title]']
        self.description = post['JSON1[description]']
        self.subject = post['JSON1[subject]'][:-1].split(',')
    def load_from_db(self,sno):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT TITLE,DESCRIPTION,OPENTIME,PAYMENT FROM SURVEY WHERE SNO = %d' % sno)
        self.title,self.description,self.opentime,self.payment = cursor.fetchone()[0:4]
        cursor.execute('SELECT PUBLICITY FROM PUBLICITY_SURVEY WHERE SNO = %d' % sno)
        self.publicity = cursor.fetchone()[0]
        db.close()

class SurveyDetail:
    def __init__(self):
        self.min_age = 0
        self.max_age = 200
        self.gender_restrict = '无限制'
        self.survey_restrict = '任何人'
        self.privacy = []
        self.payment = 0
        self.owner = ''
        self.opentime = ''
        self.maxneed = 100

    def parse(self, post, owner, submit_time):
        try:
            self.min_age = max(int(post['JSON2[min-age]']), 0)
            self.max_age = min(int(post['JSON2[max-age]']), 200)
        except ValueError:
            pass
        self.gender_restrict = post['JSON2[gender-restrict]']
        self.survey_restrict = post['JSON2[survey-restrict]']
        self.privacy = post['JSON2[privacy]'][:-1].split(',')
        self.payment = max(0, int(post['JSON2[payment]']))
        self.owner = owner
        self.opentime = submit_time
        self.maxneed = max(0,int(post['JSON2[maxneed]']))

class SurveyQuestions:
    def __init__(self):
        self.question_list = []

    class Question:
        def __init__(self):
            self.qno = -1
            self.type = ""
            self.title = ""
            self.supplement = ""
            self.supplement_type = ""
            # QA:text,number QSC:single.multiple
            self.input_type = ""
            self.choice = []
        def to_dict(self):
            return {'qno':self.qno,'type':self.type,'title':self.title,'supplement':self.supplement,'supplement_type':self.supplement_type,
                    'input_type':self.input_type,'choice':self.choice}

    def parse(self, post):
        i = 1
        while 'JSON3[%d][title]' % i in post.keys():
            q = SurveyQuestions.Question()
            q.title = post['JSON3[%d][title]' % i]
            q.type = post['JSON3[%d][type]' % i]
            q.supplement = post['JSON3[%d][supplement]' % i]
            q.supplement_type = post['JSON3[%d][suptype]' % i]
            q.input_type = post['JSON3[%d][inputtype]' % i]
            if q.type == 'qsc':
                q.choice = post['JSON3[%d][choice]' % i][:-1].split(',')
            self.question_list.append(q)
            i += 1

    def append(self,tup,choice):
        #cursor.execute("SELECT QNO,TITLE,SUPPLEMENT,SUPPLEMENT_TYPE,TYPE FROM QUESTION WHERE SNO = %d " % sno)
        q = SurveyQuestions.Question()
        q.type,q.input_type = tup[4].split(" ")
        q.qno,q.title,q.supplement,q.supplement_type = tup[0:4]
        if choice:
            for item in choice:
                q.choice.append(item[0])
        self.question_list.append(q.to_dict())

class TaskInfo:
    def __init__(self):
        self.tno = -1 #Aucson 0427
        self.title = ''
        self.description = ''
        self.deadline = ''
        self.payment = ''
        self.stage = ''
        self.owner = ''
        self.opentime = ''
    def parse(self,post,owner,time):
        self.title = post['title']
        self.description = post['description']
        self.deadline = post['deadline']
        self.payment = post['payment']
        self.owner = owner
        self.opentime = time
    def load_from_db(self,tno):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT TITLE,DESCRIPTION,OPENTIME,PAYMENT FROM TASK WHERE TNO = %d' % tno)
        self.title, self.description, self.opentime, self.payment = cursor.fetchone()[0:4]
        db.close()


def add_survey_to_db(title, detail, questions, user='root', pwd='dbpjdbpj'):
    # args type - SurveyTitle, SurveyDetail, SurveyQuestion
    db = connect_db()
    cursor = db.cursor()
    # title

    sql = "INSERT INTO SURVEY(SNO,TITLE,DESCRIPTION,MINAGE,MAXAGE,GENDER_RESTRICT,SURVEY_RESTRICT,PAYMENT,STAGE,OPENTIME,TYPE,MAXNEED) VALUES" \
          "(NULL,'%s','%s',%d,%d,'%s','%s',%d,'OPEN','%s','SURVEY',%d)" % (
          title.title, title.description, detail.min_age, detail.max_age,
          detail.gender_restrict, detail.survey_restrict, detail.payment, detail.opentime,detail.maxneed)
    cursor.execute(sql)
    cursor.execute("SELECT MAX(SNO) FROM SURVEY")
    sno = cursor.fetchall()[0][0]

    cursor.execute("SELECT UNO FROM USERINFO WHERE UNAME = '%s'" % detail.owner)
    uno = cursor.fetchall()[0][0]
    sql = "INSERT INTO SCHOLAR_OWN_SURVEY(UNO,SNO,ACCESS) VALUES(%d,%d,'owner')" % (uno, sno)
    cursor.execute(sql)

    for subject in title.subject:
        sql = "INSERT INTO SURVEY_SUBJECT(SNO,WHAT) VALUES(%d,'%s')" % (sno, subject)
        cursor.execute(sql)
    for privacy in detail.privacy:
        sql = "INSERT INTO PRIVACY(SNO,WHAT) VALUES (%d,'%s')" % (sno, privacy)
        cursor.execute(sql)
    for question in questions.question_list:
        sql = "INSERT INTO QUESTION(QNO,SNO,TITLE,SUPPLEMENT,SUPPLEMENT_TYPE,TYPE) VALUES" \
              "(NULL,%d,'%s','%s','%s','%s')" % (sno, question.title, question.supplement, question.supplement_type,
                                                 question.type + " " + question.input_type)
        cursor.execute(sql)
        if question.type == 'qsc':
            cursor.execute("SELECT MAX(QNO) FROM QUESTION")
            qno = cursor.fetchall()[0][0]
            for i, choice in enumerate(question.choice):
                sql = "INSERT INTO CHOICE(CNO,PLACE,QNO,CONTENT) VALUES(NULL,%d,%d,'%s')" % (i, qno, choice)
                cursor.execute(sql)
    db.commit()
    db.close()

def check_legibility(sno,uno):
    # whether volunteer meets requirements
    sno = int(sno)
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT MINAGE,MAXAGE,SURVEY_RESTRICT,GENDER_RESTRICT FROM SURVEY WHERE SNO = %d" % sno)
    tup = cursor.fetchone()
    min_age,max_age,sr,gr = tup[0:5]
    cursor.execute("SELECT AGE,GENDER,USERTYPE FROM USERINFO WHERE UNO = %d" % uno)
    age,gender,usertype = cursor.fetchone()[0:4]
    cursor.execute("SELECT SNO FROM PARTICIPATION WHERE UNO = %d AND SNO = %d" % (uno,sno))
    has_dup = cursor.fetchone()
    errtext = ""
    if has_dup:
        errtext = "你已经参与过调研"
        return False,errtext
    if age < min_age or age > max_age:
        errtext += "年龄不符合要求;"
    if (gr == u'仅女性' and gender == u'Male') or (gr == u'仅男性' and gender == u'Female'):
        errtext += "性别不符合要求;"
    if sr == u'仅学者' and usertype != u'Scholar':
        errtext += "身份不符合要求;"
    db.close()
    if errtext != "":
        return False,errtext
    else:
        return True,""

def inform_privacy(sno):
    sno = int(sno)
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT WHAT FROM PRIVACY WHERE SNO = %d" % sno)
    l = cursor.fetchall()
    ret = []
    for tup in l:
        ret.append(tup[0])
    db.close()
    return ret

def load_brief_summary(sno):
    sno = int(sno)
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT TITLE,DESCRIPTION,PAYMENT,INST FROM SURVEY,SCHOLAR_OWN_SURVEY,SCHOLAR WHERE "
                   "SURVEY.SNO = SCHOLAR_OWN_SURVEY.SNO AND SCHOLAR_OWN_SURVEY.UNO = SCHOLAR.UNO AND ACCESS = 'owner' "
                   "AND SURVEY.SNO = %d" %sno)
    l = cursor.fetchone()
    return {'title':l[0],'description':l[1],'payment':l[2],'inst':l[3]}

def load_questions(sno):
    sno = int(sno)
    db = connect_db()
    cursor = db.cursor()
    sq = SurveyQuestions()
    cursor.execute("SELECT QNO,TITLE,SUPPLEMENT,SUPPLEMENT_TYPE,TYPE FROM QUESTION WHERE SNO = %d ORDER BY SNO" % sno)
    tups = cursor.fetchall()
    if not tups:
        return None
    for tup in tups:
        tup2 = []
        if tup[4].startswith("qsc"):
            cursor.execute("SELECT CONTENT FROM CHOICE WHERE QNO = %d ORDER BY PLACE" % tup[0])
            tup2 = cursor.fetchall()
        sq.append(tup,tup2)
    return sq

def add_task_to_db(task=None):
    db = connect_db()
    cursor = db.cursor()

    #print task.payment

    sql = "INSERT INTO TASK(TITLE,DESCRIPTION,OPENTIME,DEADLINE,PAYMENT,TYPE,STAGE) VALUES\
          ('%s','%s','%s','%s','%s','TASK','OPEN')" % \
          (task.title,task.description,task.opentime,task.deadline,task.payment)
    #print "sql:",sql
    cursor.execute(sql)

    cursor.execute("SELECT MAX(TNO) FROM TASK")
    tno = cursor.fetchone()[0]
    #print tno
    cursor.execute("SELECT UNO FROM USERINFO WHERE UNAME = '%s'" % task.owner)
    uno = cursor.fetchone()[0]
    #print uno
    sql = "INSERT INTO SCHOLAR_OWN_TASK(UNO,TNO,ACCESS) VALUES(%d,%d,'owner')" % (uno,tno)
    cursor.execute(sql)

    db.commit()
    db.close()

    return tno

def add_file_to_db(rawdata,example,tno,datatype,num):
    db = connect_db()
    cursor = db.cursor()

    sql = "INSERT INTO FILE(FNAME,ENAME,TNO,DATATYPE) VALUES" \
          "('%s','%s',%d,'%s')" % (rawdata,example,tno,datatype)
    cursor.execute(sql)

    cursor.execute("SELECT MAX(FNO) FROM FILE")
    fno = cursor.fetchone()[0]

    for i in range(0,num):
        sql = "INSERT INTO FILE_SLICE(FNO,FSNO,SEND,RECEIVE) VALUES" \
              "(%d,%d,'0','0')" % (fno,i)
        #print "test____",sql
        cursor.execute(sql)

    db.commit()
    db.close()

