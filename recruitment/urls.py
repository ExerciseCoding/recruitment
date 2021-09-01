"""recruitment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.utils.translation import gettext as _
urlpatterns = [
    # 将jobs的urls引用进来
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    
    # 注册用户登录接口
    url('accounts/', include('registration.backends.simple.urls')),
    # path('i18n/',include('django.conf.urls.i18n')),
    url("", include("jobs.urls")),
]

# 定义站点标题 并设置多语言
admin.site.site_header = _('招聘管理系统')
