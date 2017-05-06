"""ScholarDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from CreateQ import views as CreateQ_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^new_survey/',CreateQ_view.new_survey,name = 'new_survey'),
    url(r'^post_survey/',CreateQ_view.post_survey,name = 'post_survey'),
    url(r'^new_task/',CreateQ_view.new_task,name='new_task'),
    url(r'^post_task/',CreateQ_view.post_task,name='post_task'),
    url(r'^list/', CreateQ_view.list, name='list'),
    url(r'^view_questions/',CreateQ_view.view_questions,name = 'view_question'),
    url(r'^view_files/', CreateQ_view.view_files, name='view_files'),
    url(r'^upload_slice/',CreateQ_view.upload_slice,name = 'upload_slice'),
    url(r'^download_data/',CreateQ_view.download_data,name = 'download_data'),
    url(r'^scholar_list/', CreateQ_view.scholar_list, name= 'scholar_list'),
    url(r'^new/',CreateQ_view.new_survey,name = 'home'),
    url(r'^list/',CreateQ_view.list,name = 'list'),
    url(r'^manage_survey/',CreateQ_view.manage_survey,name = 'manage_survey'),
    url(r'^manage_task/',CreateQ_view.manage_task,name = 'manage_task'),
    url(r'^download_csv/',CreateQ_view.download_csv,name = 'download_csv')
]
