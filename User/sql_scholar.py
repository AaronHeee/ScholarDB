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




