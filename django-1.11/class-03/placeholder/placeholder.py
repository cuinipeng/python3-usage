#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 运行本例:
#   django-admin.py startproject foo --template=project_template.zip
#
# 创建可复用的模板, 制作过程中会把 project_name, project_directory,
# secret_key 和 docs_version 作为上下文传递
#
import os
import sys
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf.urls import url
from django.conf import settings
from django import forms

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
# 保证 SECRET_KEY 在项目层面上是固定的, 在不同项目之间是充分随机的
SECRET_KEY = os.environ.get('SECRET_KEY', 'quf%)&tlc&0ww@l!^6gs&*j@3iaf7vwl^emqwy26jjj*87h3vs')


class ImageForm(forms.Form):
    '''
    Django Form 一般用于校验 POST 和 GET 内容.
    在这个例子中, 如果表单数据有效, 可以通过表单 cleaned_data 属性得到,
    同时两个值也会被转换成整形,保证它们介于 1 到 2000
    '''
    width = forms.IntegerField(min_value=1, max_value=2000)
    height = forms.IntegerField(min_value=1, max_value=2000)


# 创建视图
def index(request):
    return HttpResponse('INDEX')


def placeholder(request, width, height):
    # 使用 Django 表单对输入进行验证
    form = ImageForm({'width': width, 'height': height})
    if form.is_valid():
        width = form.cleaned_data['width']
        height = form.cleaned_data['height']
        return HttpResponse('%d x %d' % (width, height))
    else:
        return HttpResponseBadRequest('Invalid Image Request')


# 定义 URL 模式
urlpatterns = (
    # 捕获 URL 中的参数, 并命名 width 和 height
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
    url(r'^$', index, name='homepage'),
)


# 设置 Django 项目, 包括数据库,缓存,国际化,静态和上传资源等.
settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)


# 创建 WSGI 应用程序
application = get_wsgi_application()


# 运行示例
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)