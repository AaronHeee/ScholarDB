from django.shortcuts import render,HttpResponse
from register_scholar import  scholar_register
from django.http import HttpResponse
# Create your views here.

def scholars_register(request):
    if request.method == 'POST':
        query = ['usrname','pwd','mail','age','gender','nation','city','inst','type']
        result = [request.POST[i] for i in query]
        sqlres,log = scholar_register(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],
                         result[8],'Scholar',0)
        if(sqlres):
            return HttpResponse("Success")
        else:
            return HttpResponse("Fail due to:"+log)
    return render(request,"scholar_register_.html")

