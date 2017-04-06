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
from django.conf.urls import url
from django.contrib import admin
from User import views

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'register/scholars',views.scholars_register,name = 'scholars_register'),
    url(r'register/scholars/action',views.scholars_register,name = "scholars_register_action"),
    url(r'register/volunteers',admin.site.urls,name = 'volunteers_register'),
    url(r'login/',admin.site.urls,name = "login")
]