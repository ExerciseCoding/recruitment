from django.contrib import admin
from interview.models import Candidate
from django.http import HttpResponse
from datetime import datetime
from interview import candidate_fieldset as cf
from django.db.models import Q
import csv
import logging

logger = logging.getLogger(__name__)
exportable_fields = (
    'username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result', 'first_interviewer_user',
    'second_result', 'second_interviewer_user',
    'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user')


def export_model_as_csv(modeladmin, request, queryset):
    """导出为csv文件
       将用户在页面选择的信息导出为csv
       Args:
           modeladmin: 
           request: 获取职位详情的request
           queryset: 用户在界面选择的数据集合
       Returns:
           返回职位详情的数据和要跳转的页面
       Raises:
           DoesNotExist: An error occurred when not found job        
    """
    response = HttpResponse(content_type='text/csv')
    # 定义导出列表
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=recruitment-candidates-list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )
    for obj in queryset:
        # 单行的记录(各个字段的值),写入到csv文件
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    logger.info("%s exported %s candidate records " % (request.user, len(queryset)))
    return response


# 给export_model_as_csv函数设置别名
export_model_as_csv.short_description = u'导出为CSV文件'
# 导出导出的权限
export_model_as_csv.allowed_permissions = ('export',)

class CandidateAdmin(admin.ModelAdmin):
    # 设置页面只读字段
    # readonly_fields = ('first_interviewer_user','second_interviewer_user',)
    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    default_list_editable = ('first_interviewer_user', 'second_interviewer_user',)
    # 判断当前用户是否有导出权限
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, 'export'))
    # hr在列表页可以编辑面试官
    def get_list_editable(self, request):
        groups_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in groups_names:
            return self.default_list_editable
        return ()
    # 对于非面试官, 非HR, 获取自己是一面面试官或者二面面试官的候选人集合: s
    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(
            # Q表达式可以表示去数据库做or或者and
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user)
        )
    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    # 去掉页面不展示的字段
    exclude = ('creator', 'created_date', 'modified_date')

    # 将导入为csv的函数放入此处
    actions = [export_model_as_csv, ]
    # 定义列表页展示字段
    list_display = (
        "username", "city", "bachelor_school", "first_score", "first_result", "first_interviewer_user", "second_result",
        "second_interviewer_user", "hr_score", "hr_result", "last_editor"
    )
    # search_fields 指定那些字段用于搜索过滤 查询字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')
    # 筛选字段
    list_filter = (
        'city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user', 'second_interviewer_user',
        'hr_interviewer_user',)
    # 字段排序
    ordering = ('hr_result', 'second_result', 'first_result')

    # 一面面试官仅填写一面反馈， 二面面试官可以填写二面反馈
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return cf.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return cf.default_fieldsets_second
        return cf.default_fieldsets


admin.site.register(Candidate, CandidateAdmin)
