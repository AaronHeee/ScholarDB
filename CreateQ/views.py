#encoding=utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
# Create your views here.
from sqls import *

def new_survey(request):
    login_user = request.session.get("username", "")
    if login_user == '':
        return HttpResponseRedirect("/users/login/")
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

def list_survey(request):
    login_user = request.session.get("username", "")
    if "load" in request.GET.keys() and request.GET["load"] == 'true':
        title = request.GET.get("title",None)
        subject = request.GET.get("subject",None).split(' ')
        order = request.GET.get("order",None)
        res = get_survey_to_db(title=title, subject=subject,order=order)
        print res
        return JsonResponse(res,safe=False)

    return render(request,'list_survey.html',{"username":login_user})

def list_survey_json(request):
    dict = {}
    return JsonResponse(dict)

def complete_survey(request):
    login_user = request.session.get("username","")
    if login_user == '':
        return HttpResponseRedirect("/users/login/")
