"""为应用程序users定义url模式"""
from django.urls import path,include
from . import views

app_name='users' #命名给django区分其他应用程序。另外，即使是django提供的默认url，将其包含在应用程序users的文件后也可通过命名空间users访问。
urlpatterns=[
    #包含默认的身份验证url、
    path('',include('django.contrib.auth.urls')),
    #上面一句这里的URL模式与URL http://localhost:8000/users/login匹配，url中的单词users让django在users/ursls.py中查找，
    #单词login让他发送请求给django的默认视图login。
    #注册页面
    path('register/',views.register,name='register'),
    #上面一句话使得科研通过视图函数定义注册页面

]