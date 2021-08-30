from django.contrib import admin
from jobs.models import Job, Resume
from django.contrib import messages
from interview.models import Candidate
from datetime import datetime
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


def enter_interview_process(modeladmin, request, queryset):
    candidate_names = ""
    for resume in queryset:
        candidate = Candidate()
        # 把 obj 对象中的所有属性拷贝到 candidate 对象中:
        candidate.__dict__.update(resume.__dict__)
        candidate.created_date = datetime.now()
        candidate.modified_date = datetime.now()
        candidate_names = candidate.username + "," + candidate_names
        candidate.creator = request.user.username
        candidate.save()
    messages.add_message(request, messages.INFO, '候选人: %s 已成功进入面试流程' % (candidate_names))


enter_interview_process.short_description = u"进入面试流程"


    
class ResumeAdmin(admin.ModelAdmin):
    actions = (enter_interview_process,)
    # 
    # def image_tag(self, obj):
    #     if obj.picture:
    #         return format_html('<img src="{}" style="width:100px;height:80px;"/>'.format(obj.picture.url))
    #     return ""
    # 
    # image_tag.allow_tags = True
    # image_tag.short_description = 'Image'

    list_display = (
        'username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'master_school', 'major',
        'created_date')

    readonly_fields = ('applicant', 'created_date', 'modified_date',)

    fieldsets = (
        (None, {'fields': (
            "applicant", ("username", "city", "phone"),
            ("email", "apply_position", "born_address", "gender",), ("picture", "attachment",),
            ("bachelor_school", "master_school"), ("major", "degree"), ('created_date', 'modified_date'),
            "candidate_introduction", "work_experience", "project_experience",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)


# 注册Job models到管理后台
admin.site.register(Job, JobAdmin)

# 注册Resume models到管理后台
admin.site.register(Resume, ResumeAdmin)
