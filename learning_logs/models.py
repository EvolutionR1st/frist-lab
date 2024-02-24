from django.db import models
#模型告诉Django如何处理应用程序中存储的数据，模型就是一个类，包含属性跟方法。
from django.contrib.auth.models import User
# Create your models here.

#下面表示    用户将存储的主题    的模型：
class Topic(models.Model): #类继承于Model。
    "用户学习的主题"
    text = models.CharField(max_length = 200) #添加属性text,是CharField数据，即为文本。定义属性时要定义预留的空间
    date_added = models.DateTimeField(auto_now_add = True) #添加属性date_added，为一个DateTimeField数据，记录日期和时间的数据。
    #传递的实参auto_now_add在用户创建新主题时自动设置为当前日期和时间
    owner=models.ForeignKey(User,on_delete=models.CASCADE)#添加关联到用户的外键，用户被删除时主题也删除
    def __str__(self): #要告诉Django默认使用哪个属性显示有关主题的信息。调用方法__str__()来显示模型的简单表示
        "返回模型的字符串表示"
        return self.text

class Entry(models.Model): #类继承于基类Model
    "学到的有关某个主题的具体知识"
    #属性topic是个ForeignKey实例；属性text是个TextField实例
    # foreignkey是数据库术语，指向数据库另外一条记录，这里将每个条目关联到特定主题
    #创建每个主题Topic时，都分配了一个键（ID）。需要在两项数据之间建立联系时，Django使用与每项信息相关联的键。
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)  #实参on_delete = models.CASCADE让Django删除主题时同时删除所有关联条目，级联删除。
    text = models.TextField() #TextField长度不受限制
    date_added = models.DateTimeField(auto_now_add = True) #date_added让我们能够按创建顺序呈现条目并在条目旁放时间戳

    class  Meta: #在Entry类中嵌套Meta类，定义元数据，用于管理模型的额外信息
        #它能让我们设置特殊属性，让Django在需要时使用Entries来表示多个条目（这里指的是网页上admin界面显示多个条目时的情况）
        #没有这个类，Django将使用Entrys表示多个条目
        verbose_name_plural = 'entries' #verbose_name_plural指定复数形式是什么

    def __str__(self):  #__str__()告诉Django呈现条目时显示哪些信息
        "返回模型的字符串表示"
        return f"{self.text[:50]}..."
        #这种为f字符串，f是format设置格式的简写。在引号前加f，可将字符串中插入变量值，只要讲变量用花括号括起来
        #这里只显示前50个字符并加字符“。。。”字面表示还有剩下的