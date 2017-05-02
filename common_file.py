#encoding=utf-8
import MySQLdb
def connect_db(user = 'root',pwd = 'dbpjdbpj',db = 'ScholarDB'):
    return MySQLdb.connect("localhost",user,pwd,db,charset = 'utf8')


translation_dict = {u"真实姓名": "UNAME", u"性别": "GENDER", u"年龄": "AGE", u"国家": "NATION", u"城市": "CITY",
                    u"男性": 'Male', u"女性": 'FEMALE',u'开源':'PUBLIC',u'私有':'PRIVATE',u'等待学者审核':'pending',
                    u'被删除':'DELETED',u'调研已删除':'survey_deleted',u'已采纳':'adopted'}
translation_dict_r =  dict(zip(translation_dict.values(),translation_dict.keys()))


def scale_db_username(uno, usertype):
    return 'scholar_%d' % uno if usertype == 'Scholar' else 'volunteer_%d' % uno

def get_basic_from_session(request):
    login_user = request.session.get("username", "")
    uno = int(request.session.get("uno", 0))
    pwd = request.session.get("pwd", "")
    usertype = request.session.get("usertype", "")
    return login_user,uno,pwd,usertype