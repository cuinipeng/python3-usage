#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 创建 placeholder:
#   django-admin.py startproject placeholder --template=project_template.zip
#
# 运行 HTTP Server:
#   python placeholder.py runserver
#
# 客户端请求:
#   http://localhost:8000/image/400x300/
#
# 项目依赖:
#   图片处理: pip install Pillow
#
import os
import sys
import logging
import hashlib
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.wsgi import get_wsgi_application
# 使用 Django 的缓存工具
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf.urls import url
from django.conf import settings
from django import forms
from django.views.decorators.http import etag

logger = logging.getLogger(__name__)

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
# 保证 SECRET_KEY 在项目层面上是固定的, 在不同项目之间是充分随机的
SECRET_KEY = os.environ.get('SECRET_KEY', 'quf%)&tlc&0ww@l!^6gs&*j@3iaf7vwl^emqwy26jjj*87h3vs')
BASE_DIR = os.path.dirname(__file__)

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


class ImageForm(forms.Form):
    '''
    Django Form 一般用于校验 POST 和 GET 内容.
    在这个例子中, 如果表单数据有效, 可以通过表单 cleaned_data 属性得到,
    同时两个值也会被转换成整形,保证它们介于 1 到 2000
    '''
    width = forms.IntegerField(min_value=1, max_value=2000)
    height = forms.IntegerField(min_value=1, max_value=2000)

    def generate(self, image_format='PNG'):
        '''
        服务端缓存

        首先判断指定格式和图片尺寸的图片是否存在缓存中, 如果存在,
        直接返回缓存中的图片, 否则生成指定格式的图片并存入缓存并
        返回字节数组.

        Django 默认使用本地过程/内存缓存, 但也可以使用不同的后端.
        '''
        width = self.cleaned_data['width']
        height = self.cleaned_data['height']
        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)
        
        if content is None:
            # 通过 ImageDraw 在图片中加入文字
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft, texttop), text, fill=(255, 255, 255))

            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)

            # 保存图片在缓存中一个小时
            cache.set(key, content, 60 * 60)
            logger.warn('Save {} to django default cache'.format(key))

        return content


def generate_etag(request, width, height):
    '''根据图片的高度和宽度生成 ETag 响应头'''
    content = 'Placehodler: {0} x {1}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()


# 客户端缓存
# 使用 etag 装饰器具有视图在被访问之前进行 ETag 计算的优势.
# 浏览器会收到 304 Not Modified 响应
@etag(generate_etag)
def placeholder(request, width, height):
    # 使用 Django 表单对输入进行验证
    form = ImageForm({'width': width, 'height': height})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('Invalid Image Request')


# 创建视图
def index(request):
    return HttpResponse('INDEX')


# 定义 URL 模式
urlpatterns = (
    # 捕获 URL 中的参数, 并命名 width 和 height
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
    url(r'^$', index, name='homepage'),
)


# 创建 WSGI 应用程序
application = get_wsgi_application()


# 运行示例
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
