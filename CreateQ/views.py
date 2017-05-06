# encoding=utf-8
import os, tempfile, zipfile
from  wsgiref.util import FileWrapper
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,HttpResponseNotFound,StreamingHttpResponse,HttpResponseForbidden,FileResponse
# Create your views here.
import os
from sqls import *
from sqls_list import *
from sqls_view import *
from sqls_scholar_list import *
from files import *
from sqls_ans import *
from User.sql_scholar import search_scholar_by_name
from User.userctrl import get_money
init_path = "/home/aaron/Desktop/Files"

def new_survey(request):
    login_user,uno,pwd,usertype = get_basic_from_session(request)
    money = get_money(uno)
    able = True
    if login_user == '':
        return HttpResponseRedirect("/users/login/")
    if usertype != 'Scholar':
        able = False
    if request.method == "POST":
        dict = request.POST
        print dict
        # 解析
        survey_title = SurveyTitle()
        survey_title.parse(request.POST)
        survey_detail = SurveyDetail()
        survey_detail.parse(request.POST, login_user, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        survey_questions = SurveyQuestions()
        survey_questions.parse(request.POST)
        money_need = survey_detail.maxneed * survey_detail.payment
        print money_need
        if money_need > money:
            return HttpResponse("你看起来余额不足,但是ScholarDB Alpha测试阶段允许透支")
        add_survey_to_db(survey_title, survey_detail, survey_questions, user='scholar_%d' % uno, pwd=pwd)
        return HttpResponse("发布成功")
    else:
        return render(request, 'create_survey.html', {"username": login_user,"able":able})

def post_survey(request):
    return HttpResponse("fail")

def view_questions(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    if login_user == "":
        return HttpResponseRedirect('/users/login/')
    if request.method == 'GET':
        sno = request.GET.get("sno", -1)
        if sno == -1:
            return HttpResponse("Survey error")
        if "load" in request.GET.keys() and request.GET["load"] == 'true':
            sq = load_questions(sno)
            if sq == None:
                return HttpResponse("Survey not exists")
            return JsonResponse(sq.question_list,safe =False)
        if "check" in request.GET.keys() and request.GET["check"] == 'true':
            json ={}
            json['result'],json['errtext'] = check_legibility(sno,uno)
            json['privacy'] = inform_privacy(sno)
            json['abstract'] = load_brief_summary(sno)
            return JsonResponse(json,safe = False)
        return render(request, 'view_questions.html', {'username': login_user, 'sno': sno})
    if request.method == 'POST':
        dict = request.POST
        print dict
        sa = SurveyAnswer()
        sa.parse(dict,uno,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        sa.add_to_db()
        return HttpResponse("Success")

def view_files(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    if request.method == 'GET':
        tno = request.GET.get("tno", -1)
        if "getInfo" in request.GET.keys():
            json = load_taskinfo(tno)
            json['init_path'] = init_path
            print json
            return JsonResponse(json,safe = False)

    return render(request, 'view_files.html',{'username':login_user,'tno':tno})

def complete_survey(request):
    login_user = request.session.get("username", "")
    if login_user == '':
        return HttpResponseRedirect("/users/login/")

# for new_task
def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print "成功创建目录：",path

def write(path,data):
    destination = open(path, 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in data.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

def upload_data(request,uno,tno):
    rawdata = request.FILES.get("rawdata", None)  # 获取上传的文件，如果没有文件，则默认为None
    example = request.FILES.get("example", None)

    if not rawdata or not example:
        print "No file upload!"
        return False

    path = os.path.join(init_path,"uno_"+str(uno),"tno_"+str(tno))
    print path

    mkdir(os.path.join(path,"sender","rawdata"))
    mkdir(os.path.join(path,"sender","example"))
    mkdir(os.path.join(path,"receiver"))

    write(os.path.join(path,"sender","rawdata",rawdata.name),rawdata)  # 打开特定的文件进行二进制的写操作
    write(os.path.join(path, "sender", "example", example.name), example)  # 打开特定的文件进行二进制的写操作

    print "upload over!"
    return rawdata.name,example.name

def new_task(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    able =True
    if login_user == '':
        return HttpResponseRedirect("/users/login/")
    if usertype != 'Scholar':
        able = False
    if request.method == "POST":
        taskinfo = TaskInfo()
        taskinfo.parse(request.POST, login_user, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        tno = add_task_to_db(taskinfo)
        rawdata,example = upload_data(request,uno,tno)
        path = os.path.join(init_path,"uno_"+str(uno),"tno_"+str(tno), "sender", "rawdata")
        print path
        num,datatype_suffix = divide_file(path,rawdata)
        datatype = get_datatype(datatype_suffix)
        print 'datatype:',datatype
        print 'num:',num
        add_file_to_db(rawdata,example,tno,datatype,num)
        # 解析
        return render(request, 'create_task.html', {"username": login_user,"able":able})
    else:
        print request.method
        return render(request, 'create_task.html', {"username": login_user,"able":able})

def post_task(request):
    return HttpResponse("fail")

def list(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    if login_user == '':
        return HttpResponseRedirect("/users/login/")
    if "load" in request.GET.keys() and request.GET["load"] == 'true':
        subject = request.GET.get("subject", None).split(' ')
        datatype = request.GET.get("datatype", None)
        print "datatype:",datatype
        order = request.GET.get("order",None)
        type = request.GET.get("type",None)
        print order
        res = get_list_from_db(subject=subject,datatype=datatype,type=type, order=order, user=scale_db_username(uno, usertype),pwd=pwd)
        return JsonResponse(res, safe=False)

    if "search" in request.GET.keys() and request.GET["search"] == 'true':
        subject = request.GET.get("subject", None).split(' ')
        datatype = request.GET.get("datatype", None)
        type = request.GET.get("type",None)
        order = request.GET.get("order", None)
        pattern = request.GET.get("pattern",None)
        isDesc = request.GET.get("isDesc",None)
        res = search(subject=subject, datatype=datatype, type=type, pattern=pattern, order=order, isDesc=isDesc, user=scale_db_username(uno, usertype), pwd=pwd)
        print res
        return JsonResponse(res, safe=False)

    return render(request, 'list.html', {"username": login_user})

def scholar_list(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    if login_user == '':
        return HttpResponseRedirect("/users/login/")
    if "load" in request.GET.keys() and request.GET["load"] == 'true':
        subject = request.GET.get("subject", None).split(' ')
        datatype = request.GET.get("datatype", None)
        publicity = request.GET.get("publicity", None)
        order = request.GET.get("order",None)
        type = request.GET.get("type",None)
        res = get_scholar_list_from_db(uno=uno, subject=subject,datatype=datatype,publicity=publicity,type=type, order=order, user=scale_db_username(uno, usertype),pwd=pwd,onlyforme=False)
        return JsonResponse(res, safe=False)

    if "search" in request.GET.keys() and request.GET["search"] == 'true':
        subject = request.GET.get("subject", None).split(' ')
        datatype = request.GET.get("datatype", None)
        type = request.GET.get("type",None)
        order = request.GET.get("order", None)
        pattern = request.GET.get("pattern",None)
        isDesc = request.GET.get("isDesc",None)
        res = search(uno=uno, subject=subject, datatype=datatype, type=type, pattern=pattern, order=order, isDesc=isDesc, user=scale_db_username(uno, usertype), pwd=pwd)
        print res
        return JsonResponse(res, safe=False)

    return render(request, 'scholar_list.html', {"username": login_user})

def scholar_list(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    if login_user == '':
        return HttpResponseRedirect("/users/login/")
    if "load" in request.GET.keys() and request.GET["load"] == 'true':
        subject = request.GET.get("subject", None).split(' ')
        datatype = request.GET.get("datatype", None)
        print "datatype:",datatype
        order = request.GET.get("order",None)
        type = request.GET.get("type",None)
        print order
        res = get_scholar_list_from_db(uno=uno, subject=subject,datatype=datatype,type=type, order=order, user=scale_db_username(uno, usertype),pwd=pwd,onlyforme=False)
        return JsonResponse(res, safe=False)

    if "search" in request.GET.keys() and request.GET["search"] == 'true':
        subject = request.GET.get("subject", None).split(' ')
        datatype = request.GET.get("datatype", None)
        type = request.GET.get("type",None)
        order = request.GET.get("order", None)
        pattern = request.GET.get("pattern",None)
        isDesc = request.GET.get("isDesc",None)
        res = search(uno=uno, subject=subject, datatype=datatype, type=type, pattern=pattern, order=order, isDesc=isDesc, user=scale_db_username(uno, usertype), pwd=pwd)
        print res
        return JsonResponse(res, safe=False)

    return render(request, 'scholar_list.html', {"username": login_user})


def manage_survey(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    access = ''
    able = True
    if login_user == '':
        return HttpResponseRedirect("/users/login/")
    if request.method == 'GET':
        sno = request.GET.get("sno",-1)
        sno = int(sno)
        tno = int(request.GET.get("tno",-1))
        override_task = False
        if sno != -1:
            no = sno
        elif tno != -1:
            no = tno
            override_task = True
        else:
            return HttpResponse("Survey/Task error")
        if sno != -1 and tno != -1:
            return HttpResponse("Ambiguous request")
        try:
            summary = load_summary_management(no,override_task)
        except TypeError: # not found sno/tno
            return HttpResponse("Project not found")
        #check authorization
        if not check_authorization(uno,no,['OWNER','COOPERATOR'],override_task):
            if summary['stage'] == 'OPEN' or summary['publicity'] == u'私有':
                able = False
        if check_authorization(uno,no,['OWNER'],override_task):
            access = 'OWNER'
        if "load_contributor" in request.GET.keys():
            json = load_contributor(no,override_task)
            print json
            return JsonResponse(json,safe = False)
        if "load_by_user" in request.GET.keys():
            if sno != -1:
                sa = SurveyAnswer()
                json = sa.to_json_list_by_user(no)
            else:
                json = to_json_list_by_user_task(no)
            return JsonResponse(json,safe=False)
        if "load_summary" in request.GET.keys():
            return JsonResponse(summary,safe=False)
        if "delete_id" in request.GET.keys():
            tuno = int(request.GET['delete_id'][1:])
            print tuno
            delete_answer(tuno,no,override_task)
            return HttpResponse("Success")
        if "search_user" in request.GET.keys():
            name = request.GET['name']
            json = search_scholar_by_name(name)
            print json
            return JsonResponse(json,safe = False)
        if "add_contributor" in request.GET.keys():
            uno = int(request.GET['uno'])
            add_contributor(uno,no,override_task)
        if "close" in request.GET.keys():
            publicity = request.GET['publicity'].replace(",","")
            print publicity
            if check_authorization(uno,no,['OWNER'],override_task):
                close_project(no,publicity,override_task)
                return HttpResponse("修改成功")
        if "delete" in request.GET.keys():
            if check_authorization(uno, no, ['OWNER']):
                delete_project(no,override_task)
                return HttpResponse("修改成功")

        if "load_date_number" in request.GET.keys():
            json = load_date_number(no,override_task)
            print json
            return JsonResponse(json, safe=False)
        if "load_gender" in request.GET.keys():
            json = load_gender(no,override_task)
            print "gender:",json
            return JsonResponse(json, safe=False)
        if "load_location" in request.GET.keys():
            json = load_location(no,override_task)
            print "location:",json
            return JsonResponse(json, safe=False)

        if "load_choice" in request.GET.keys():
            json = load_choice(sno)
            return JsonResponse(json,safe=False)
        #用于加载相关性的可选选项信息：
        if "load_option" in request.GET.keys():
            json = load_option(sno)
            print "options:",json
            return JsonResponse(json,safe=False)
        if "load_correlaion" in request.GET.keys():
            variable_1 = request.GET.get("variable_1", -1)
            variable_2 = request.GET.get("variable_2", -1)
            json = load_correlation(sno,variable_1,variable_2)
            return JsonResponse(json,safe=False)

        return render(request,'manage_survey.html',{'username':login_user,'sno':sno,'tno':tno,'access':access,
                                                    'able':able,'is_task':override_task})

def manage_task(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    access = ''
    able = True
    if login_user == '':
        return HttpResponseRedirect("/users/login/")
    if request.method == 'GET':
        sno = request.GET.get("sno",-1)#记得修改回来
        sno = int(sno)
        tno = int(request.GET.get("tno",-1)) #也记得修改回来
        override_task = False
        if sno != -1:
            no = sno
        elif tno != -1:
            no = tno
            override_task = True
        else:
            return HttpResponse("Survey/Task error")
        if sno != -1 and tno != -1:
            return HttpResponse("Ambiguous request")
        try:
            summary = load_summary_management(no,override_task)
        except TypeError: # not found sno/tno
            return HttpResponse("Project not found")
        #check authorization
        if not check_authorization(uno,no,['OWNER','COOPERATOR'],override_task):
            if summary['stage'] == 'OPEN' or summary['publicity'] == u'私有':
                able = False
        if check_authorization(uno,no,['OWNER'],override_task):
            access = 'OWNER'
        if "download_all" in request.GET.keys():
            path = os.path.join(init_path, "uno_" + str(uno), "tno_" + str(tno))
            newpath = os.path.join(path, 'data.zip')
            if os.path.exists(newpath):
                os.remove(newpath)
            f = zipfile.ZipFile(newpath, 'w', zipfile.ZIP_DEFLATED)
            for dirpath, dirnames, filenames in os.walk(os.path.join(path,"receiver")):
                for filename in filenames:
                    f.write(os.path.join(dirpath, filename))
            f.close()
            return JsonResponse({},safe=False)
        if "load_contributor" in request.GET.keys():
            json = load_contributor(no,override_task)
            print "json",json
            return JsonResponse(json,safe = False)
        if "load_by_user" in request.GET.keys():
            if sno != -1:
                sa = SurveyAnswer()
                json = sa.to_json_list_by_user(no)
            else:
                json = to_json_list_by_user_task(no)
            return JsonResponse(json,safe=False)
        if "load_summary" in request.GET.keys():
            return JsonResponse(summary,safe=False)
        if "delete_id" in request.GET.keys():
            tuno = int(request.GET['delete_id'][1:])
            print tuno
            if sno != -1:
                delete_answer(tuno, no)
            return HttpResponse("Success")
        if "search_user" in request.GET.keys():
            name = request.GET['name']
            json = search_scholar_by_name(name)
            print json
            return JsonResponse(json,safe = False)
        if "add_contributor" in request.GET.keys():
            uno = int(request.GET['uno'])
            add_contributor(uno,no,override_task)
        if "close" in request.GET.keys():
            publicity = request.GET['publicity'].replace(",","")
            print publicity
            if check_authorization(uno,no,['OWNER'],override_task):
                close_project(no,publicity,override_task)
                return HttpResponse("修改成功")
        if "delete" in request.GET.keys():
            if check_authorization(uno, no, ['OWNER']):
                delete_project(no,override_task)
                return HttpResponse("修改成功")
        if "load_slice" in request.GET.keys():
            tno = request.GET.get("tno",-1)
            if tno == -1:
                return HttpResponse("未找到该任务")

            json = load_slice(tno)
            return JsonResponse(json, safe=False)
        return render(request, 'manage_task.html', {'username': login_user, 'sno': sno, 'tno': tno, 'access': access,
                                                      'able': able, 'is_task': override_task})


def download_csv(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    try:
        sno = int(request.GET.get("sno", -1))
    except TypeError:
        return HttpResponse("Invalid sno")
    if sno == -1:
        return HttpResponseNotFound("Survey not found")
    try:
        summary = load_summary_management(sno)
    except TypeError:  # not found sno/tno
        return HttpResponse("Survey not found")
    if not check_authorization(uno, sno, ['OWNER', 'COOPERATOR']):
        if summary['stage'] == 'OPEN' or summary['publicity'] == u'私有':
            return HttpResponseForbidden("You have not access for the file")
    sa = SurveyAnswer()
    filename = 'scholardb_survey_export_%d.csv' % sno
    f = sa.to_csv(sno,filename = filename)
    response =  StreamingHttpResponse(f.read().encode('utf-8'))
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = f.tell()

    f.close()
    os.remove(filename)
    return response

def download_data(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    tno = request.GET.get("tno", -1)
    uno_2 = request.GET.get("uno", -1)
    num = request.GET.get("num",-1)
    max_num = request.GET.get("max_num",-1)

    path = os.path.join(init_path,"uno_"+str(uno_2),"tno_"+str(tno),"sender","rawdata")
    index = send_index(max_num,num,tno,uno)

    os.remove(os.path.join(path,'data.zip'))

    f = zipfile.ZipFile(os.path.join(path,'data.zip'), 'w', zipfile.ZIP_DEFLATED)
    for i in index:
        filename = str(i)+".zip"
        print filename
        f.write(os.path.join(path,filename),filename)
    f.close()

    res = {}
    res['tno'] = tno
    res['uno'] = uno

    return JsonResponse(res, safe=False)



    #打包成压缩文件下发

def upload_slice(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    tno = request.POST['tno']
    uno_2 = request.POST['uno']
    able = True
    if login_user == '':
        return HttpResponseRedirect("/users/login/")
    if usertype != 'Scholar':
        able = False
    if request.method == "POST":
        slice = request.FILES.get("rawdata_slice",None)
        if not slice:
            print "No file upload!"

        path = os.path.join(init_path, "uno_" + str(uno_2), "tno_" + str(tno),"receiver",str(uno))
        mkdir(path)
        write(os.path.join(path,slice.name),slice)

        sql_upload_slice(tno,uno,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        print "upload over!"
        # 解析
        return render(request, 'create_task.html', {"username": login_user, "able": able})
    else:
        print request.method
        return render(request, 'create_task.html', {"username": login_user, "able": able})


