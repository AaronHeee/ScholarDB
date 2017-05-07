#encoding=utf-8
import MySQLdb
from common_file import connect_db

def load_taskinfo(tno):
    db = connect_db()
    cursor = db.cursor()

    json = {}

    sql = "SELECT UNO,TITLE,DESCRIPTION,PAYMENT,DEADLINE,EXAMPLE_NAME FROM TASK T, SCHOLAR_OWN_TASK S,FILE F WHERE T.TNO = S.TNO AND T.TNO = F.TNO AND S.TNO = %s" % tno
    cursor.execute(sql)

    res = cursor.fetchone()

    json['uno'] = res[0]
    json['title'] = res[1]
    json['description'] = res[2]
    json['payment'] = res[3]
    json['deadline'] = res[4]
    json['example_name'] = res[5]

    sql = "SELECT COUNT(FSNO) FROM FILE F, FILE_SLICE S WHERE F.FNO = S.FNO AND F.TNO = %s GROUP BY F.FNO"% tno
    #print sql
    cursor.execute(sql)
    res = cursor.fetchone()
    json['num'] = res[0]

    db.close()
    return json

def send_index(max_num,num,tno,uno):
    db = connect_db()
    cursor = db.cursor()

    max_num = int(max_num)
    num = int(num)
    uno = int(uno)

    sql = "SELECT SEND FROM FILE F, FILE_SLICE S WHERE F.FNO = S.FNO AND F.TNO = %s "% tno
    cursor.execute(sql)

    res = cursor.fetchall()
    for i in range(0,max_num):
        j = i
        i = (i+1)%max_num
        if res[i][0] < res[j][0]:
            break

    index = []

    for k in range(0,num):
        index.append(i)
        i = (i+1)%max_num

    sql = "SELECT FNO FROM FILE F WHERE F.TNO = %s " % tno
    cursor.execute(sql)

    fno = int(cursor.fetchone()[0])

    for k in index:
        sql = "UPDATE FILE_SLICE,FILE SET SEND = SEND + 1 WHERE FILE_SLICE.FNO = FILE.FNO AND FILE.TNO = %s AND FSNO = %d"%(tno,k)
        cursor.execute(sql)

        sql = "INSERT INTO PARTICIPATION_TASK(FNO,FSNO,UNO,STATUS) VALUES (%d,%d,%d,'unload')" % (fno,k,uno)
        cursor.execute(sql)

    #print "fno",fno
    #print "tno",tno

    db.commit()
    db.close()

    #print index
    return index

def sql_upload_slice(tno,uno,submit_time):
    db = connect_db()
    cursor = db.cursor()

    tno = int(tno)
    uno = int(uno)

    sql = "SELECT FNO FROM FILE F WHERE F.TNO = %s " % tno
    cursor.execute(sql)

    fno = int(cursor.fetchone()[0])

    sql = "UPDATE PARTICIPATION_TASK SET STATUS='pending',SUBMIT_TIME='%s' WHERE FNO=%d AND UNO=%d"% (submit_time,fno,uno)
    #print sql
    cursor.execute(sql)

    sql = "SELECT FSNO FROM PARTICIPATION_TASK WHERE FNO=%d AND UNO=%d" % (fno,uno)
    cursor.execute(sql)

    res = cursor.fetchall()
    for i in res:
        sql = "UPDATE FILE_SLICE SET RECEIVE=RECEIVE+1 WHERE FNO=%d AND FSNO=%d" % (fno,i[0])
        #print sql
        cursor.execute(sql)

    db.commit()
    db.close()








