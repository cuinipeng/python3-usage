#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pip install Pillow
#
import random
from PIL import Image, ImageFilter, ImageDraw, ImageFont

filename = 'lol-gailun.jpg'
output_filename = 'output.jpg'
output_format = 'jpeg'

# 基本操作, 缩放/切片/旋转/滤镜/输出文字
print('==> 缩放图片')
im = Image.open(filename)
(width, height) = im.size
print('{0}: {1}x{2}'.format(filename, width, height))
print('缩放 {0} 到 1/4'.format(filename))
im.thumbnail((width / 4, height / 4))
im.save(output_filename, output_format)
im.close()

# 模糊图像
print('==> 模糊图片')
im = Image.open(filename)
im2 = im.filter(ImageFilter.BLUR)
im2.save(output_filename, output_format)
im2.close()
im.close()

# 制作验证码, 绘图
print('==> 制作验证码')
def rndBgColor():
    return (random.randint(64, 255),
            random.randint(64, 255),
            random.randint(64, 255))
def rndTextColor():
    return (random.randint(32, 127),
            random.randint(32, 127),
            random.randint(32, 127))
def rndChar():
    return chr(random.randint(65, 90))

width = 60 * 4
height = 60

im = Image.new('RGB', (width, height), (255, 255, 255)) # 白色背景
font = ImageFont.truetype('C:\\Windows\\Fonts\\Arial.ttf', 36)
draw = ImageDraw.Draw(im)

# 随机填充背景
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rndBgColor())

for t in range(4):
    draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndTextColor())
    # draw.text((60 * t + 10, 10), rndChar(), fill=rndTextColor())

im = im.filter(ImageFilter.BLUR)
im.save(output_filename, output_format)
im.close()
