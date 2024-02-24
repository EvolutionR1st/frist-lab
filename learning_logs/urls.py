"定义learning_logs的URL模式"
#上面的说明旨在说明当前是哪个urls.py文件
from django.urls import path #path能够将URL映射到视图
from . import views #句点让python从使用的urls.py模块所在文件夹导入view.py

app_name = 'learning_logs' #app_name让Django区分项目内同名的urls.py文件
urlpatterns = [
    #主页
    path('',views.index,name = 'index'),
    #显示所有主题
    path('topics/', views.topics ,name = 'topics'),
    #特定主题的详细页面
    path('topics/<int:topic_id>/',views.topic,name='topic'),#第一个''中的topics让Django查找在基础URL后跟着topics的URL，
    #<int:topic_id>与包含在两个斜杠内的整数匹配，再将整数匹配到topic_id的实参中
    #若URL与该模式匹配，Django调用views中的topic()，并将储存在topic_id中的实参传递给topic()。在该函数中，将使用topic_id的值获取相应主题。
    path('new_topic/', views.new_topic, name='new_topic'),
    #用于添加新条目的页面
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),#同样地<int:topic_id>捕获数值并给变量topic_id
    #用于编辑条目的页面
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry')
]
#urlpatterns是列表，包含可在应用程序learning_logs中请求的页面
#实际的URL模式为对函数path()的调用，函数接受三个实参 。
#第一个实参为一个字符串，帮助Django正确地路由（route）请求。
#收到请求的 URL后，Django力图 将请求 路由给一个视图。会 搜索所有 的 URL模式，找到与当前请求匹配的那个。
#Django忽视项目基础URL（http://localhost:8000）,因此空字符串''与 基础URL匹配。如果请求的 URL与任何既有RUL模式都不匹配，返回一个错误
#第二个实参为请求的URL与前述正则表达式匹配时调用oview.py中函数index（）
#第三个实参将这个URL模式的名称指定 为index，让我们在代码 的 其他地方能引用他。需要提供主页链接时，都将使用这个名称而不编写URL。