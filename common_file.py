#encoding=utf-8
import MySQLdb
def connect_db(user = 'root',pwd = 'dbpjdbpj',db = 'ScholarDB'):
    return MySQLdb.connect("localhost",user,pwd,db,charset = 'utf8')


translation_dict = {u"真实姓名": "UNAME", u"性别": "GENDER", u"年龄": "AGE", u"国家": "NATION", u"城市": "CITY",
                    u"男性": 'Male', u"女性": 'FEMALE'}
translation_dict_r =  dict(zip(translation_dict.values(),translation_dict.keys()))