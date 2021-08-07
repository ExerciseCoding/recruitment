from django.contrib import admin
from jobs.models import Job


# Register your models here.

# 定义页面显示的时候的字段
class JobAdmin(admin.ModelAdmin):
    # exclude 页面上除去那些字段，设置完后不会保存到数据库
    exclude = ('creator', 'created_date', 'modifield_date')
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'created_date', 'modifield_date')

    # 解决exclude不会保存字段到数据库
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


# 注册Job models到管理后台
admin.site.register(Job, JobAdmin)
