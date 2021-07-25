#
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
JobTypes = [
    (0,"技术类"),
    (1,"产品类"),
    (2,"运营类"),
    (3,"设计类")
]

Cities = [
    (0,"北京"),
    (1,"上海"),
    (2,"深圳")
]
# Create your models here.
class Job(models.Model):
    # verbose_name 对象的可读名称，choices 提供被选数据，它默认解析为一个下来菜单，对于静态的下拉菜单式很方便
    job_type = models.SmallIntegerField(blank=False, choices=JobTypes, verbose_name="职位类别")
    job_name = models.CharField(max_length=250, blank=False, verbose_name="职位名称")
    job_city = models.SmallIntegerField(choices=Cities, blank=False,verbose_name="工作地点")
    job_responsibility = models.TextField(max_length=1024,verbose_name="职位职责")
    job_requirement = models.TextField(max_length=1024,blank=False, verbose_name="职位要求")
    # 创建人为系统用户,因此使用外键引用，on_delete 外键引用所以当用户被删除时，这条数据SET_NULL被设置为NULL
    creator = models.ForeignKey(User,verbose_name="创建人", on_delete = models.SET_NULL, null = True)
    created_date = models.DateTimeField(verbose_name="创建日期",default=datetime.now)
    modifield_date = models.DateTimeField(verbose_name="修改时间",default=datetime.now)


