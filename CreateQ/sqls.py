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

    def parse(self, post):
        self.title = post['JSON1[title]']
        self.description = post['JSON1[description]']
        self.subject = post['JSON1[subject]'][:-1].split(',')


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
        # 多值属性！

    def parse(self, post, owner, time):
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
            # QA:text,number QSC:single.multiple
            self.input_type = ""
            self.choice = []
        def to_dict(self):
            return {'type':self.type,'title':self.title,'supplement':self.supplement,'supplement_type':self.supplement_type,
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
        print self.question_list

    def append(self,tup,choice):
        #cursor.execute("SELECT QNO,TITLE,SUPPLEMENT,SUPPLEMENT_TYPE,TYPE FROM QUESTION WHERE SNO = %d " % sno)
        q = SurveyQuestions.Question()
        q.type,q.input_type = tup[4].split(" ")
        q.title,q.supplement,q.supplement_type = tup[1:4]
        if choice:
            for item in choice:
                q.choice.append(item[0])
        self.question_list.append(q.to_dict())

def add_survey_to_db(title, detail, questions, user='root', pwd='dbpjdbpj'):
    db = connect_db()
    cursor = db.cursor()
    # title

    sql = "INSERT INTO SURVEY(SNO,TITLE,DESCRIPTION,MINAGE,MAXAGE,GENDER_RESTRICT,SURVEY_RESTRICT,PAYMENT,STAGE,OPENTIME) VALUES" \
          "(NULL,'%s','%s',%d,%d,'%s','%s',%d,'OPEN','%s')" % (
          title.title, title.description, detail.min_age, detail.max_age,
          detail.gender_restrict, detail.survey_restrict, detail.payment, detail.opentime)
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
              "(NULL,%d,'%s','%s','%s', '%s')" % (sno, question.title, question.supplement, question.supplement_type,
                                                 question.type+" "+ question.input_type)
        cursor.execute(sql)
        if question.type == 'qsc':
            cursor.execute("SELECT MAX(QNO) FROM QUESTION")
            qno = cursor.fetchall()[0][0]
            for i, choice in enumerate(question.choice):
                sql = "INSERT INTO CHOICE(CNO,PLACE,QNO,CONTENT) VALUES(NULL,%d,%d,'%s')" % (i, qno, choice)
                cursor.execute(sql)
    db.commit()
    db.close()

def add_survey_to_db(title, detail, questions, user='root', pwd='dbpjdbpj'):
    db = connect_db()
    cursor = db.cursor()
    # title

    sql = "INSERT INTO SURVEY(SNO,TITLE,DESCRIPTION,MINAGE,MAXAGE,GENDER_RESTRICT,SURVEY_RESTRICT,PAYMENT,STAGE,OPENTIME) VALUES" \
          "(NULL,'%s','%s',%d,%d,'%s','%s',%d,'OPEN','%s')" % (
          title.title, title.description, detail.min_age, detail.max_age,
          detail.gender_restrict, detail.survey_restrict, detail.payment, detail.opentime)
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
              "(NULL,%d,'%s','%s','%s', '%s')" % (sno, question.title, question.supplement, question.supplement_type,
                                                 question.type+" "+ question.input_type)
        cursor.execute(sql)
        if question.type == 'qsc':
            cursor.execute("SELECT MAX(QNO) FROM QUESTION")
            qno = cursor.fetchall()[0][0]
            for i, choice in enumerate(question.choice):
                sql = "INSERT INTO CHOICE(CNO,PLACE,QNO,CONTENT) VALUES(NULL,%d,%d,'%s')" % (i, qno, choice)
                cursor.execute(sql)
    db.commit()
    db.close()


def get_survey_from_db(title=None, subject=None, order=None, user='root', pwd='dbpjdbpj'):
    db = connect_db()
    cursor = db.cursor()


    sql = """CREATE TEMPORARY TABLE LIST (
                LNO INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                SNO INTEGER,
                TNO INTEGER,
                TITLE VARCHAR(200) NOT NULL,
                DESCRIPTION VARCHAR(200) NOT NULL,
                PAYMENT INTEGER NOT NULL,
                OPENTIME DATETIME NOT NULL,
                MINAGE SMALLINT,
                MAXAGE SMALLINT,
                GENDER_RESTRICT VARCHAR(45),
                SURVEY_RESTRICT VARCHAR(45) 
                )"""
    cursor.execute(sql)
    cursor.execute("alter table LIST convert to character set utf8;")


    sql = "SELECT SNO,TITLE,MINAGE,MAXAGE,GENDER_RESTRICT,SURVEY_RESTRICT,OPENTIME,PAYMENT,DESCRIPTION FROM SURVEY "
    condition = []
    if title != None and title != '':
        condition.append("TITLE LIKE '%" + title + "%'")
    if subject != [None] and subject != [''] and subject != []:
        for sub in subject:
            if sub == '' or sub == ' ':
                continue
            condition.append("SNO IN (SELECT SNO FROM SURVEY_SUBJECT WHERE WHAT = '%s')" % sub)
    if condition != None and condition != []:
        sql += ' WHERE '
        sql += ' AND '.join(condition)
    if order == None:
        order = 'SNO DESC'
    sql += ' ORDER BY %s' % (order)
    cursor.execute(sql)
    sql_res = cursor.fetchall()

    sql = "INSERT INTO LIST(SNO,TITLE,MINAGE,MAXAGE,GENDER_RESTRICT,SURVEY_RESTRICT,OPENTIME,PAYMENT,DESCRIPTION)" + sql
    cursor.execute(sql)

    cursor.execute("SELECT * FROM LIST")
    sql_list = cursor.fetchall()
    print "==============\n"
    print sql_list

    res = []
    for tup in sql_res:
        dict = {"sno": tup[0], "title": tup[1], "min_age": tup[2], "max_age": tup[3], "gender_restrict": tup[4],
                "survey_restrict": tup[5], "opentime": tup[6], "payment": tup[7], "description": tup[8]}
        sql = "SELECT WHAT FROM SURVEY_SUBJECT WHERE SNO = %d" % tup[0]
        cursor.execute(sql)
        l = cursor.fetchall()
        dict["subject1"] = l[0][0] if len(l) >= 1 else ""
        dict["subject2"] = l[1][0] if len(l) >= 2 else ""
        dict["subject3"] = l[2][0] if len(l) >= 3 else ""
        res.append(dict)
    db.close()
    return res

def check_legibility(sno,uno):
    # whether volunteer meets requirements
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT MINAGE,MAXAGE,SURVEY_RESTRICT,GENDER_RESTRICT FROM SURVEY WHERE SNO = %d" % sno)
    tup = cursor.fetchone()
    min_age,max_age,sr,gr = tup[0:5]
    cursor.execute("SELECT AGE,GENDER,USERTYPE FROM USERINFO WHERE UNO = %d" % uno)
    age,gender,usertype = cursor.fetchone()[0:4]
    errtext = ""
    if age < min_age or age > max_age:
        errtext += "年龄不符合要求;"
    if (gr == '仅女性' and gender == 'Male') or (gr == '仅男性' and gender == 'Female'):
        errtext += "性别不符合要求;"
    if sr == '仅学者' and usertype != 'Scholar':
        errtext += "身份不符合要求;"
    db.close()
    if errtext != "":
        return False,errtext
    else:
        return True,""

def inform_privacy(sno):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT WHAT FROM PRIVACY WHERE SNO = %d" % sno)
    l = cursor.fetchall()
    text = ""
    for tup in l:
        text+= tup[0] + ' '
    db.close()
    return text

def load_brief_summary(sno):
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
    for tup in tups:
        tup2 = []
        if tup[4].startswith("qsc"):
            cursor.execute("SELECT CONTENT FROM CHOICE WHERE QNO = %d ORDER BY PLACE" % tup[0])
            tup2 = cursor.fetchall()
        sq.append(tup,tup2)
    return sq


class TaskInfo:
    def __init__(self):
        self.title = ''
        self.description = ''
        self.deadline = ''
        self.payment = ''
        self.stage = ''
        self.owner = ''
        self.opentime = ''
        self.rawdata = ''
        self.example = ''
    def parse(self,post,rawdata,example,owner,time):
        self.title = post['title']
        self.description = post['description']
        self.deadline = post['deadline']
        self.payment = post['payment']
        self.rawdata = rawdata
        self.example = example
        self.owner = owner
        self.opentime = time


def add_task_to_db(task):
    db = connect_db()
    cursor = db.cursor()

    print task.payment

    sql = "INSERT INTO TASK(TITLE,DESCRIPTION,OPENTIME,DEADLINE,PAYMENT) VALUES\
          ('%s','%s','%s','%s','%s')" % \
          (task.title,task.description,task.opentime,task.deadline,task.payment)
    cursor.execute(sql)

    cursor.execute("SELECT MAX(TNO) FROM TASK")
    tno = cursor.fetchone()[0]
    print tno
    cursor.execute("SELECT UNO FROM USERINFO WHERE UNAME = '%s'" % task.owner)
    uno = cursor.fetchone()[0]
    print uno
    sql = "INSERT INTO SCHOLAR_OWN_TASK(UNO,TNO,ACCESS) VALUES(%d,%d,'owner')" % (uno,tno)
    cursor.execute(sql)

    sql = "INSERT INTO FILE(RAWDATA,EXAMPLE,NUM,NOW) VALUES " \
          "('%s','%s', 100, 0)" % (task.rawdata, task.example)
    cursor.execute(sql)
    cursor.execute("SELECT MAX(FNO) FROM FILE")
    fno = cursor.fetchone()[0]
    print fno
    sql = "INSERT INTO TASK_WITH_FILE(TNO,FNO) VALUES (%d, %d)" % (tno,fno)
    cursor.execute(sql)

    db.commit()
    db.close()


def add_survey_to_list(title=None, subject=None, user='root', pwd='dbpjdbpj'):
    db = connect_db()
    cursor = db.cursor()

    sql = "SELECT SNO,TITLE,OPENTIME,PAYMENT,DESCRIPTION FROM SURVEY "
    condition = []
    if title != None and title != '':
        condition.append("TITLE LIKE '%" + title + "%'")
    if subject != [None] and subject != [''] and subject != []:
        for sub in subject:
            if sub == '' or sub == ' ':
                continue
            condition.append("SNO IN (SELECT SNO FROM SURVEY_SUBJECT WHERE WHAT = '%s')" % sub)
    if condition != None and condition != []:
        sql += ' WHERE '
        sql += ' AND '.join(condition)

    return sql

def add_task_to_list(user='root', pwd='dbpjdbpj'):
    db = connect_db()
    cursor = db.cursor()

    sql = "SELECT TNO,TITLE,OPENTIME,PAYMENT,DESCRIPTION FROM TASK "
    condition = []
    if condition != None and condition != []:
        sql += ' WHERE '
        sql += ' AND '.join(condition)

    return sql

def load_json(list_res):
    db = connect_db()
    cursor = db.cursor()
    res = []
    for tup in list_res:
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

    db.commit()
    db.close()

    return res


def get_list_from_db(title=None, subject=None, order=None, user='root', pwd='123456'):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'ScholarDB' AND table_name = 'LIST' ")
    l = cursor.fetchall();
    print l
    if(l[0][0]==1):
        cursor.execute("DROP TABLE LIST")

    sql = """CREATE TABLE LIST (
                LNO INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                NO INTEGER,
                TYPE VARCHAR(20),
                TITLE VARCHAR(200) NOT NULL,
                DESCRIPTION VARCHAR(200) NOT NULL,
                PAYMENT INTEGER NOT NULL,
                OPENTIME DATETIME NOT NULL
                )"""

    cursor.execute(sql)
    cursor.execute("alter table LIST convert to character set utf8;")

    sql_survey = add_survey_to_list(title,subject,user,pwd)
    sql = "INSERT INTO LIST(NO,TITLE,OPENTIME,PAYMENT,DESCRIPTION)" + sql_survey
    cursor.execute(sql)
    cursor.execute("UPDATE LIST SET TYPE='SURVEY'")

    sql_task = add_task_to_list(user,pwd)
    sql = "INSERT INTO LIST(NO,TITLE,OPENTIME,PAYMENT,DESCRIPTION)" + sql_task
    cursor.execute(sql)

    cursor.execute("UPDATE LIST SET TYPE='TASK' WHERE TYPE IS NULL")

    sql = "SELECT TYPE,NO,TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM LIST ORDER BY " + order
    cursor.execute(sql)

    list_res = cursor.fetchall()

    print list_res

    res = load_json(list_res)

    db.commit()
    db.close()

    return res

def order_list(order=None, user='root',pwd=123456):
    db = connect_db()
    cursor = db.cursor()

    sql = "SELECT TYPE,NO,TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM LIST ORDER BY " + order
    cursor.execute(sql)

    list_res = cursor.fetchall()
    res = load_json(list_res)

    db.close()

    return res

def subject_list(subject=None,order=None,user='root',pwd=123456):
    db = connect_db()
    cursor = db.cursor()

    sql = "DELETE FROM LIST WHERE TYPE='SURVEY' AND ( "
    condition = []
    for sub in subject:
        if sub == '' or sub == ' ':
            continue
        condition.append("NO NOT IN (SELECT SNO FROM SURVEY_SUBJECT WHERE WHAT = '%s')" % sub)
    sql += ' OR '.join(condition)
    sql += ")"

    cursor.execute(sql)
    sql = "SELECT TYPE,NO,TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM LIST ORDER BY " + order
    cursor.execute(sql)

    list_res = cursor.fetchall()
    res = load_json(list_res)

    db.commit()
    db.close()

    return res


def datatype_list(datatype=None, order=None,user='root', pwd=123456):
    db = connect_db()
    cursor = db.cursor()

    sql = "DELETE FROM LIST WHERE TYPE='TASK' AND "
    sql += "NO NOT IN (SELECT TNO FROM TASK_WITH_FILE,FILE WHERE FILE.FNO = TASK_WITH_FILE.FNO AND DATATYPE = '%s')" % datatype

    print "-------------================"
    print sql

    cursor.execute(sql)
    sql = "SELECT TYPE,NO,TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM LIST ORDER BY " + order
    cursor.execute(sql)

    list_res = cursor.fetchall()
    res = load_json(list_res)

    db.commit()
    db.close()

    return res


def type_list(type=None, order=None, user='root', pwd=123456):
    db = connect_db()
    cursor = db.cursor()

    if type=='TASK':
        sql = "DELETE FROM LIST WHERE TYPE='SURVEY'"

    if type=='SURVEY':
        sql = "DELETE FROM LIST WHERE TYPE='TASK'"

    cursor.execute(sql)
    sql = "SELECT TYPE,NO,TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM LIST ORDER BY " + order
    cursor.execute(sql)

    list_res = cursor.fetchall()
    res = load_json(list_res)

    db.commit()
    db.close()

    return res

def search(pattern=None, order=None, isDesc=None, user='root', pwd=123456):
    db = connect_db()
    cursor = db.cursor()

    sql = "SELECT TYPE,NO,TITLE,DESCRIPTION,PAYMENT,OPENTIME FROM LIST WHERE TITLE LIKE '%" + pattern + "%'"
    if isDesc:
        sql += "OR DESCRIPTION LIKE '%" + pattern + "%'"
    sql += "ORDER BY " + order

    print sql

    cursor.execute(sql)

    list_res = cursor.fetchall()
    res = load_json(list_res)

    db.commit()
    db.close()

    return res

