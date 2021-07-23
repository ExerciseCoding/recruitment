from django.shortcuts import render
from jobs.models import Cities, JobTypes
from jobs.models import Job
from django.template import loader
from django.http import HttpResponse
# Create your views here.
def joblist(request):
    job_list = Job.objects.order_by('job_type')
    template = loader.get_template('joblist.html')
    context = {'job_list': job_list}
    for job in job_list:
        job.city_name = Cities[job.job_city][1]
        job.type_name = JobTypes[job.job_type][1]
    return HttpResponse(template.render(context))