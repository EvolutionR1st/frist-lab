from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    """注册新用户"""
    if request.method != 'POST':
        #显示空的注册表单
        form =UserCreationForm()
    else:
        #处理填写好的表单
        form=UserCreationForm(data=request.POST) #根据提交的数据创建USerCreationForm实例

        if form.is_valid():
            #本用例的有效是指名字未包含非法字符，输入的两个密码相同
            new_user=form.save()
            #让用户自动登录，再重定向到主页
            login(request,new_user)
            return redirect('learning_logs:index')#重定向到主页

    #显示空表单或指出表单无效
    context={'form':form}
    return render(request,'registration/register.html',context)