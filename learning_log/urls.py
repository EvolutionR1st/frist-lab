"""
URL configuration for learning_log project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

#变量urlpatterns包含项目中应用程序的URL
#模块admin.site.urls定义 了可在管理网站中请求的所有URL
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')), #与任何以单词users打头的url都匹配
    path('',include('learning_logs.urls'))
]
