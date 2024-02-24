from django.shortcuts import render, redirect
#函数render（）根据视图 提供的数据渲染响应,redirect为重定向用，将视图名作为参数并重定向到该视图
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic,Entry #导入与数据相关的模型
from .forms import TopicForm, EntryForm

# Create your views here.在这里创建视图，view.py是在运行命令python manage.py startapp时自动生成的
#视图函数接受请求中的信息，使用定义页面外观的模板，准备好生成页面所需数据，再将 这些数据 发送给服务器
#当learning_logs的程序运行时，匹配了模式，Django将在views.py中查找函数index()，再将对象request传递给视图函数
def index(request):
    "学习笔记的主页"
    return render(request,'learning_logs/index.html')  #这里有两个实参，一个是对象request，另外一个是 可用于创建页面的模板

@login_required
#未登录时通过settings中的LOGIN_URL中的变量重定向
def topics(request): #形参为Django从服务器收到的request对象
    "显示所有主题"
    #topics = Topic.objects.order_by('date_added')
    # 查询数据库，请求提供Topic对象，并根据属性date_added排序,返回的查询集储存在topics中
    topics = Topic.objects.filter(ower=request.user).order_by('date_added')
    # 用户登录后，request对象将有一个user属性，储存有关该用户的信息，查询Topic.objects.filter(ower=request.user)让Django只从
    #数据库中获取owner属性为当前用户的Topic对象。
    context = {'topics' : topics}
    #context为定义将发送给模板的上下文（上下文是个字典）。键--将在模板中用来访问数据的名称，值--发送给模板的数据。注意这里只有一个键值对。
    return render(request,'learning_logs/topics.html',context) #除了对象request跟模板路径外，还将变量context传递给render（）。

@login_required
def topic(request, topic_id): #除了request对象外，还包含在urls.py由/<int:topic_id>/捕获的形参topic_id。
    "显示单个主题及所有条目"
    topic = Topic.objects.get(id=topic_id) #使用get()获取指定的主题号，这行跟下一行entries都为查询代码，向数据库查询。不过可在Django shell先尝试，快速反馈。
    #确认请求的主题属于当前用户,渲染前检查
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added') #获取与主题关联的条目，因为有"-"，根据date_added进行降序排序
    context = {'topic': topic,'entries':entries} #主题跟条目都储存到了字典context
    return render(request,'learning_logs/topic.html',context) #把字典传给了模板topic.html

@login_required
def new_topic(request):
    #用户初次请求该页面时，浏览器会发送get请求，用户填写提交表单时浏览器发送POST请求。
    """添加新主题"""
    if request.method != 'POST': #确定请求方法是get还是post
        #未提交数据：创建一个新表单
        form = TopicForm()#实例化topicform没指定任何参数，django将创建空表单给用户写
    else:
        #post提交的数据，对数据进行处理
        form=TopicForm(data=request.POST)
        if form.is_valid(): #提交的信息是否有效需要验证，如填写所有必不可少字段与字段长度大小是否超限
            new_topic = form.save(commit=False)#实参的作用是-先修改新主题再保存
            new_topic.owner = request.user#读取request里的user再设置为当前主题的owner
            new_topic.save()#完事后再调用默认save
            #form.save()
            return redirect('learning_logs:topics')

    #显示空表单或指出表单数据无效
    context={'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    #用户初次请求该页面时，浏览器会发送get请求，用户填写提交表单时浏览器发送POST请求。
    """在特定主题添加新条目"""
    topic=Topic.objects.get(id=topic_id)#需要知道针对哪个主题所作操作

    if request.method != 'POST': #确定请求方法是get还是post
        #未提交数据：创建一个新表单
        form = EntryForm()#实例化Entryform没指定任何参数，django将创建空表单给用户写
    else:
        #post提交的数据，对数据进行处理
        form=EntryForm(data=request.POST)
        if form.is_valid(): #提交的信息是否有效需要验证，如填写所有必不可少字段与字段长度大小是否超限
            new_entry=form.save(commit=False)#commit=false让django创建新条目对象赋给new_entry但不保存到数据库
            new_entry.topic=topic#将属性topic设置为函数开头获取的主题
            new_entry.save() #这里才保存到数据库并与正确主题关联
            return redirect('learning_logs:topic',topic_id=topic_id)#重定向到视图函数topic还需要实参topic_id

    #显示空表单或指出表单数据无效
    context={'topic':topic, 'form':form} #这是上下文字典
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有条目"""
    #第一步先获取条目与关联的主题
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    #获取指定的条目，检查条目关联的主题所有者是否是当前登录用户
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #初次请求：使用当前条目填充表单
        #使用实参instance=entry创建EntryForm实例，创建表单实例并用条目对象的信息填充它
        #用户能看到数据并能编辑
        form=EntryForm(instance=entry)
    else:
        #POST提交的数据：对数据进行处理
        form=EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save() #这里不指定任何实参因为已经关联到特定条目了
            return redirect('learning_logs:topic',topic_id=topic.id)

    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)