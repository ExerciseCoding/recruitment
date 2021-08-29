from django.shortcuts import render
from jobs.models import Cities, JobTypes
from jobs.models import Job
from django.template import loader
from django.http import HttpResponse
from django.http import Http404


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
