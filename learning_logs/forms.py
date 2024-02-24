from django import forms

from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}

class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry#表单基于的模型
        fields = ['text']#表单包含的字段
        labels = {'text':''}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}
        #widget小部件，是一个html表单元素，如单行文本框，多行文本区域或下拉列表
        #使用forms.Textarea，定制了text的宽度为80列，默认为40.