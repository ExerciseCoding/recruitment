from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from jobs.models import Cities, JobTypes
from jobs.models import Job, Resume


# Create your views here.
def joblist(request):
    """获取职位列表
    查询所以得职位并返回给前端渲染
    Args:
        request: 获取职位列表的请求信息
    Returns:
        返回列表并跳转到列表页面    
    """
    job_list = Job.objects.order_by('job_type')
    template = loader.get_template('joblist.html')
    context = {'job_list': job_list}
    for job in job_list:
        job.city_name = Cities[job.job_city][1]
        job.type_name = JobTypes[job.job_type][1]
    return render(request, 'joblist.html', context)


def detail(request, job_id):
    """获取职位详情
    根据职位id查询职位详情
    Args:
        request: 获取职位详情的request
        job_id: 职位id
    Returns:
        返回职位详情的数据和要跳转的页面
    Raises:
        DoesNotExist: An error occurred when not found job        
    """
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    return render(request, 'job.html', {'job': job})


class ResumeDetailView(DetailView):
    """   简历详情页    """
    model = Resume
    template_name = 'resume_detail.html'


# LoginRequiredMixin支持多继承 CreateView django自带的创建视图的view
class ResumeCreateView(LoginRequiredMixin, CreateView):
    """ 简历职位页面
    创建简历的view

    Attributes:
        template_name: 创建简历的模板页面
        success_url: 
        model: 指定简历model
    """
    template_name = 'resume_form.html'
    success_url = '/joblist/'
    model = Resume
    fields = ["username", "city", "phone",
              "email", "apply_position", "gender",
              "bachelor_school", "master_school", "major", "degree", "picture", "attachment",
              "candidate_introduction", "work_experience", "project_experience"]

    ### 从 URL 请求参数带入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
