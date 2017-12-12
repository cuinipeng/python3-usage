#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 运行本例:
#   python quickstart.py runserver
#
# 这个例子提供了 Django 框架一些基础知识, 如编写视图, 创建设置, 运行管理命令等.
# Django 的核心是 Python 框架, 用于处理 HTTP 请求并返回 HTTP 输出, 至于过程要做什么, 完全取决与你.
#
# Django 还提供了一些用于处理 HTTP 请求中所设计的常见任务的工具,
# 例如渲染 HTML, 分析表单数据和持久化保持会话状态.
#
#
import os
import sys
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.conf.urls import url
from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))


# 创建视图
def index(request):
    html = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>Lightweight Django</title>
</head>
<body>
<h3>Hello World</h3>
</body>
</html>
    '''
    return HttpResponse(html.strip())


# 定义 URL 模式
urlpatterns = (
    url(r'^$', index),
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