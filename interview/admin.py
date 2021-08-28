from django.contrib import admin
from interview.models import Candidate
from django.http import HttpResponse
from datetime import datetime
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
            return ('first_interviewer_user','second_interviewer_user',)
        return ()

    default_list_editable = ('first_interviewer_user', 'second_interviewer_user',)
    # hr在列表页可以编辑面试官
    def get_list_editable(self, request):
        groups_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in groups_names:
            return self.default_list_editable
        return ()
    
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
    # 页面字段显示太多，进行分类
    # ("username", "city", "phone", "email") 用元组括起来表示放在一行
    default_fieldsets = (
        (None, {'fields': ("userid", ("username", "city", "phone"), ("email", "apply_position", "born_address"),
                           ("gender", "candidate_remark"),
                           ("bachelor_school", "master_school", "doctor_school", "major", "degree"),
                           ("test_score_of_general_ability", "paper_score"), "last_editor",
                           )}),
        ('第一轮面试记录', {'fields': (
            ("first_score", "first_learning_ability", "first_professional_competency"), "first_advantage",
            "first_disadvantage", "first_result", "first_recommend_position", "first_interviewer_user", "first_remark",
        )}),
        ('第二轮面试记录', {'fields': (
            ("second_score", "second_learning_ability"),
            ("second_professional_competency", "second_pursue_of_excellence"),
            ("second_communication_ability", "second_pressure_score"), "second_advantage", "second_disadvantage",
            "second_result", "second_recommend_position", "second_interviewer_user", "second_remark",
        )}),
        ('第三轮面试记录', {'fields': (("hr_score", "hr_responsibility", "hr_communication_ability"),
                                ("hr_logic_ability", "hr_potential", "hr_stability"), "hr_advantage", "hr_disadvantage",
                                "hr_result", "hr_interviewer_user", "hr_remark",)}),
    )

    # 一面面试官编辑时显示的内容
    default_fieldsets_first = (
        (None, {'fields': ("userid", ("username", "city", "phone"), ("email", "apply_position", "born_address"),
                           ("gender", "candidate_remark"),
                           ("bachelor_school", "master_school", "doctor_school", "major", "degree"),
                           ("test_score_of_general_ability", "paper_score"), "last_editor",
                           )}),
        ('第一轮面试记录', {'fields': (
            ("first_score", "first_learning_ability", "first_professional_competency"), "first_advantage",
            "first_disadvantage", "first_result", "first_recommend_position", "first_interviewer_user", "first_remark",
        )}),
    )
    # 二面面试官编辑时显示的内容
    default_fieldsets_second = (
        (None, {'fields': ("userid", ("username", "city", "phone"), ("email", "apply_position", "born_address"),
                           ("gender", "candidate_remark"),
                           ("bachelor_school", "master_school", "doctor_school", "major", "degree"),
                           ("test_score_of_general_ability", "paper_score"), "last_editor",
                           )}),
        ('第一轮面试记录', {'fields': (
            ("first_score", "first_learning_ability", "first_professional_competency"), "first_advantage",
            "first_disadvantage", "first_result", "first_recommend_position", "first_interviewer_user", "first_remark",
        )}),
        ('第二轮面试记录', {'fields': (
            ("second_score", "second_learning_ability"),
            ("second_professional_competency", "second_pursue_of_excellence"),
            ("second_communication_ability", "second_pressure_score"), "second_advantage", "second_disadvantage",
            "second_result", "second_recommend_position", "second_interviewer_user", "second_remark",
        )}),
    )
    # 一面面试官仅填写一面反馈， 二面面试官可以填写二面反馈
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return self.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return self.default_fieldsets_second
        return self.default_fieldsets




admin.site.register(Candidate, CandidateAdmin)
