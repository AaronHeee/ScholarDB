from django.shortcuts import render,HttpResponse
from userctrl import register,login_mail,get_name
from django.http import HttpResponse
# Create your views here.

def scholars_register(request):
    if request.method == 'POST':
        query = ['usrname','pwd','mail','age','gender','nation','city','inst','type']
        result = [request.POST[i] for i in query]
        sqlres,log = register(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],
                         result[8],'Scholar',0)
        if(sqlres):
            return HttpResponse("Success")
        else:
            return HttpResponse("Fail due to:"+log)
    return render(request,"scholar_register_.html")

def login(request):
    login_user = request.session.get("username","")
    if login_user:
        return HttpResponse("Success:"+login_user)
    elif request.method == 'POST':
        mail = request.POST['mail']
        pwd = request.POST['pwd']
        res,log = login_mail(mail,pwd)
        print mail,pwd
        if not res:
            return HttpResponse("Fail" + log)
        else:
            if 'auto' in request.POST:
                login_user = request.session["username"] = get_name(mail)
            return HttpResponse("Success" + login_user)
    return render(request,"login.html",{"username:":login_user})