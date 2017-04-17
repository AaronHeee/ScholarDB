#encoding=utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
import os
from sqls import *

def new_survey(request):
    login_user = request.session.get("username", "")
    login_user = "金熙森"
    if login_user == '':
        return HttpResponse("Forbidden")
    if request.method == "POST":
        dict = request.POST
        print dict
        #解析
        survey_title = SurveyTitle()
        survey_title.parse(request.POST)
        survey_detail = SurveyDetail()
        survey_detail.parse(request.POST,login_user,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        survey_questions = SurveyQuestions()
        survey_questions.parse(request.POST)
        add_survey_to_db(survey_title,survey_detail,survey_questions)
        return HttpResponse("??")
    else:
        return render(request,'create_survey.html',{"username":login_user})

def post_survey(request):
    return HttpResponse("fail")

def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        print request.FILES
        myFile =request.FILES.get("rawdata", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return render(request, 'test.html')
        destination = open(os.path.join("/home/aaron/Desktop",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        return render(request, 'test.html')
    else:
        return render(request, 'test.html')

def upload_data(request,name):
    myFile = request.FILES.get("rawdata", None)  # 获取上传的文件，如果没有文件，则默认为None
    if not myFile:
        print "No file upload!"
    destination = open(os.path.join("/home/aaron/Desktop/receiver",name+"/"+myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    print "upload over!"
    return os.path.join("/home/aaron/Desktop/receiver",name+"/"+myFile.name)

def new_task(request):
    login_user = request.session.get("username", "")
    login_user = "金熙森"
    if login_user == '':
        return HttpResponse("Forbidden")
    if request.method == "POST":
        print request.FILES
        rawdata = upload_data(request,"rawdata")
        example = upload_data(request,"example")
        # 解析
        taskinfo = TaskInfo()
        print request.POST
        taskinfo.parse(request.POST, rawdata, example, login_user, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        add_task_to_db(taskinfo)
        return render(request, 'create_task.html', {"username": login_user})
    else:
        print request.method
        return render(request, 'create_task.html', {"username": login_user})

def post_task(request):
    return HttpResponse("fail")