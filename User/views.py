# encoding=utf-8
from django.shortcuts import render,HttpResponse
from userctrl import register,login_mail,get_basic_info
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from common_file import *
from sql_index import *
from sql_scholar import *
# Create your views here.

def index(request):
    login_user, uno, pwd, usertype = get_basic_from_session(request)
    if request.method == 'GET':
        if 'load_statistics' in request.GET.keys():
            return JsonResponse(get_statistics())
        if 'load_public_survey' in request.GET.keys():
            min = int(request.GET['min'])
            max = int(request.GET['max'])
            json_list = get_public_survey(min,max)
            print json_list
            return JsonResponse(json_list,safe=False)
        if 'load_public_task' in request.GET.keys():
            min = int(request.GET['min'])
            max = int(request.GET['max'])
            json_list = get_public_task(min, max)
            print json_list
            return JsonResponse(json_list, safe=False)

    return render(request, "index.html", {"username": login_user})

def scholars_register(request):
    login_user = request.session.get("username", "")
    if request.method == 'POST':
        query = ['usrname','pwd','mail','age','gender','nation','city','inst','type']
        result = [request.POST[i] for i in query]
        sqlres,log = register(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],
                         result[8],'Scholar',0)
        if(sqlres):
            return HttpResponseRedirect('/users/login/')
        else:
            return HttpResponse("Fail due to:"+log)
    return render(request,"scholar_register_.html",{"username":login_user})

def volunteer_register(request):
    login_user = request.session.get("username", "")
    if request.method == 'POST':
        query = ['usrname','pwd','mail','age','gender','nation','city']
        result = [request.POST[i] for i in query]
        sqlres,log = register(result[0],result[1],result[2],result[3],result[4],result[5],result[6],'','','Volunteer',0)
        if(sqlres):
            return HttpResponseRedirect('/users/login/')
        else:
            return HttpResponse("Fail due to:"+log)
    return render(request,"volunteer_register_.html",{"username":login_user})

def login(request):
    login_user = request.session.get("username","")
    if request.method == 'POST':
        mail = request.POST['mail']
        pwd = request.POST['pwd']
        res,log = login_mail(mail,pwd)

        print mail,pwd
        if not res:
            return render(request,"good_login.html",{"errtext":log})
        else:
            request.session["username"],request.session["uno"],request.session["usertype"] = get_basic_info(mail)
            request.session["pwd"] = pwd
            login_user = request.session.get("username","")
            return HttpResponseRedirect("/")
    return render(request,"good_login.html",{"username:":login_user})

def user_info(request):
    login_user,uno,pwd,usertype = get_basic_from_session(request)
    if login_user == '':
        return HttpResponseRedirect("/users/login/")

    if request.method == 'GET':
        target_uno = int(request.GET.get('tuno',uno))
        target_usertype = get_user_type(target_uno)
        if 'load_user_info' in request.GET.keys():
            if target_usertype == 'Scholar':
                s = Scholar()
                s.load_basic_info_from_db(target_uno)
                return JsonResponse(s.to_json(restrict=not target_uno == uno))
            elif target_usertype == 'Volunteer':
                v = Volunteer()
                v.load_basic_info_from_db(target_uno)
                return JsonResponse(v.to_json(restrict=not target_uno == uno))
        if 'load_project_info' in request.GET.keys() and target_usertype == 'Scholar':
            return JsonResponse(project_list_of_scholar(target_uno),safe=False)
        if 'load_participation_info' in request.GET.keys():
            return JsonResponse(participation_list(target_uno),safe=False)
        return render(request,"scholar_detail.html",{'username':login_user,'uno':uno,'tuno':target_uno,
                                                     'usertype':usertype,'tusertype':target_usertype})

def logout(request):
    try:
        del request.session["username"]
        del request.session["pwd"]
        del request.session["uno"]
    except KeyError:
        pass
    return HttpResponseRedirect("/")

def document(request):
    return render(request,"scholardb_document.html")

def document_content(request):
    return render(request,"document_content.htm")

def easter_egg(request):
    return HttpResponse("OH!YOU FOUND THE EASTER EGG!")