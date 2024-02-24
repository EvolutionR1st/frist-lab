from django.contrib import admin

# Register your models here.在这注册你的模型

#这是注册模型topic的代码
from .models import Topic,Entry#首先导入要注册的模型, 句号+models让Django在admin.py所在目录查找models.py

admin.site.register(Topic)  #register让Django通过管理网站管理模型
admin.site.register(Entry)  #register让Django通过管理网站管理模型,注册了模型/model：Entry
