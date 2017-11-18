#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import etree

text = ""
with open("index.html", "r") as fd:
    text = fd.read()

# 从字符串构建
# html = etree.HTML(text)
# result = etree.tostring(html)
# print(result.decode("utf-8"))

# 文件读取
html = etree.parse("index.html")
result = etree.tostring(html, pretty_print=True)
# print(result.decode("utf-8"))

# XPath 测试
result = html.xpath("//li")
result = html.xpath("//li/@class")
print(result)
