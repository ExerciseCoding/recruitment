from django.conf.urls import url
from django.urls import path
from jobs import views

urlpatterns = [
    # 职位列表
    url(r"^joblist", views.joblist, name="joblist"),
    url(r"^job/(?P<job_id>\d+)/$", views.detail, name="detail"),
    path('resume/add/', views.ResumeCreateView.as_view(), name='resume-add'),
    path('resume/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),
    url(r"^", views.joblist, name="name")
]
