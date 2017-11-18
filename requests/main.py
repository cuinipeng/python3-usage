#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import requests
from requests import Request, Session
from requests.auth import AuthBase, HTTPBasicAuth, HTTPDigestAuth

###############################################################################
#
# 快速上手
#   ref: http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
#
###############################################################################

# 1. 发送请求
# r = requests.get("https://httpbin.org")
# r = requests.post("https://httpbin.org/post")
# r = requests.put("https://httpbin.org/put")
# r = requests.delete("https://httpbin.org/delete")
# r = requests.head("https://httpbin.org/get")
# r = requests.options("https://httpbin.org/get")
# print(r.text, r.context, r.json())


# 2. 传递 URL 参数
payload = {"key1": "value1", "key2": "value2"}
payload = {"key1": "value1", "key2": ["value2", "value3"]}
payload = {"key1": "value1", "key2": ["value2", "value3"], "key3": None}
# r = requests.get("https://httpbin.org/get", params=payload)
# print(r.text)


# 3. 响应内容
# r = requests.get("https://github.com/timeline.json")
# r.encoding = "ISO-8859-1"
# print(r.encoding, r.text)


# 4. 二进制响应内容, 自动解码 gzip 和 deflate 数据
# r = requests.get("https://github.com/timeline.json")
# print(type(r.content))


# 5. JSON 响应内容
# r = requests.get("https://github.com/timeline.json")
# print(r.json())


# 6. 原始响应内容
filename = "timeline.json"
chunk_size = 4096
# r = requests.get("https://github.com/timeline.json", stream=True)
# print(r.raw, type(r.raw))
# print(r.raw.read(10))
# with open(filename, "wb") as fd:
#     for chunk in r.iter_content(chunk_size):
#        fd.write(chunk)


# 7. 定制请求头
"""
Host: httpbin.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache

User-Agent: python-requests/2.18.4
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
"""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Host": "httpbin.org",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate"
}
# r = requests.get("https://httpbin.org/get", headers=headers)
# print(r.request.headers)
# print(r.text)


# 8. 更加复杂的 POST 请求
# payload = {"key1": "value1", "key2": "value2"}
# payload = (("key1", "value1"), ("key2", "value2"))
# r = requests.post("https://httpbin.org/post", headers=headers, data=payload)
# r = requests.post("https://httpbin.org/post", headers=headers, data=json.dumps(payload))
# print(r.text)


# 9. POST 一个多部分编码(Multipart-Encoded)的文件
"""
如果你发送一个非常大的文件作为 multipart/form-data 请求,
你可能希望将请求做成数据流. 默认下 requests 不支持, 但有
个第三方包 requests-toolbelt 是支持的.

$ tcpdump -i ens33 -w multipart.pcap port 80

{
  "Host": "httpbin.org",
  "Cache-Control": "no-cache",
  "Content-Length": "528",
  "Accept-Encoding": "gzip, deflate",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
  "Pragma": "no-cache",
  "Connection": "keep-alive",
  "Content-Type": "multipart/form-data; boundary=8827deebdc234f009f1d234215a0c7d1",
}
"""
filename = "timeline.json"
files = {"file": "file data"}
files = {"file": open(filename, "rb")}
files = {"file": (filename, open(filename, "rb"), "application/octet-stream", {"Expires": "0"})}
# r = requests.post("http://httpbin.org/post", headers=headers, files=files)
# print(json.dumps(dict(r.request.headers), indent=2))
# print(r.text)


# 10. 响应状态码
# r = requests.get("https://httpbin.org/get")
# print(r.status_code == requests.codes.ok)
# r = requests.get("https://httpbin.org/status/404")
# print(r.raise_for_status())


# 11. 响应头
# r = requests.get("https://httpbin.org/get", headers=headers)
# print(r.headers.get("Content-Type"))


# 12. Cookie
cookies = requests.cookies.RequestsCookieJar()
cookies.set("tasty", "yum", domain="httpbin.org", path="/cookies")
cookies.set("gross", "blech", domain="httpbin.org", path="/elsewhere")
# r = requests.get("https://httpbin.org/cookies", cookies=cookies)
# print(json.dumps(dict(r.request.headers), indent=2))
# print(r.text)


# 13. 重定向与请求历史
# r = requests.get("http://github.com", allow_redirects=True)
# print(r.url, r.status_code, r.history)


# 14. 超时
# r = requests.get("https://github.com", timeout=3)
# print(r)




###############################################################################
#
# 高级用法
#   ref: http://docs.python-requests.org/zh_CN/latest/user/advanced.html
#
###############################################################################
# 1. 会话对象
# s = requests.Session()
# r = s.get("https://httpbin.org/cookies/set/sessioncookie/123456789")
# r = s.get("https://httpbin.org/cookies")
# print(r.text)

# s.auth = ("user", "pass")
# s.headers.update({"x-test": "true"})
# s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"})
# r = s.get("https://httpbin.org/headers", headers={"x-test-2": "true"})
# print(json.dumps(dict(r.request.headers), indent=2))
# with requests.Session() as s:
#     s.get("https://httpbin.org/cookies/set/sessioncookie/123456789")


# 2. 准备的请求(Prepared Request)
# s = Session()
# req = Request("GET", "https://httpbin.org/get", data=None, headers=headers)
# <class 'requests.models.PreparedRequest'>
# prepedreq = req.prepare()
# prepedreq = s.prepare_request(req)
# r = s.send(prepedreq, stream=True, verify=True, proxies=None, cert=None, timeout=5)
# print(r.status_code)


# SSL 证书验证
# with requests.Session() as s:
#     # REQUEST_CA_BUNDLE
#     # s.verify = "/etc/pki/tls/certs/ca-bundle.crt"
#     r = s.get("https://httpbin.org/get", verify=True)
#     print(r)


# 客户端证书 - 单个文件(包含密钥和证书)或一个包含两个文件路径的元组.
# 本地证书的私有 key 必须是解密状态. 目前, Requests 不支持使用加密的 key.
# with requests.Session() as s:
#     # 或者保存客户端证书在会话中
#     # s.cert = "/path/client.cert"
#     r = s.get("https://httpbin.org/get", cert=("/path/client.cert", "/path/client.key"))
#     print(r)


# CA 证书
# requests 默认附带了一套它自己新人的根证书, 来自 Mozilla Trust Store
# (https://hg.mozilla.org/mozilla-central/raw-file/tip/security/nss/lib/ckfw/builtins/certdata.txt)
# /usr/lib/python3.4/site-packages/certifi/cacert.pem


# 响应体内容工作流
# 默认情况下,当你进行网络请求后,响应体会立即被下载.
# 可以通过 stream 参数覆盖这个行为,推迟下载响应体直到访问 Response.content 属性.
TOO_LONG = 0xffffffff
tarball_url = "https://github.com/kennethreitz/requests/tarball/master"
tarball_url = "https://github.com/requests/requests/tarball/master"
# with requests.Session() as s:
#     r = s.get(tarball_url, stream=True)
#     # 仅有响应头被下载下来了,连接保持打开状态.
#     if int(r.headers["Content-Length"]) < TOO_LONG:
#         print(r.headers["Content-Length"])
#         content = r.content


# 流式上传
# with requests.Session() as s:
#     with open(filename, "rb") as fd:
#         r = s.post("https://httpbin.org/post", data=fd)
#         print(r.text)

# POST 多个分块编码的文件
# <input type="file" name="images" multiple="true" required="true" />
"""
<!DOCTYPE HTML>
<html>
<head>
    <meta charset="utf-8" />
    <title>Multiple Post Files Example</title>
</head>
<body>
    <form method="POST"  enctype="multipart/form-data" action="https://httpbin.org/post">
        <input type="file" name="image" required="true" /><br />
        <input type="file" name="images" multiple="true" required="true" /><br />
        <input type="submit" value="Upload">
    </form>
</body>
</html>
"""
url = "https://httpbin.org/post"
filenames = ["HTTP-Post-Single-File-Header-01.jpg", "HTTP-Post-Single-File-Header-02.jpg"]
multiple_files = [
    ("images", (filenames[0], open(filenames[0], "rb"), "image/jpeg")),
    ("images", (filenames[1], open(filenames[1], "rb"), "image/jpeg"))
]
filenames = ["1.txt", "2.txt", "3.txt"]
multiple_files = [
    ("mulfiles", (filenames[0], open(filenames[0], "rb"), "text/plain")),
    ("mulfiles", (filenames[1], open(filenames[1], "rb"), "text/plain")),
    ("mulfiles", (filenames[2], open(filenames[2], "rb"), "text/plain"))
]
# with requests.Session() as s:
#     r = s.post(url, files=multiple_files)
#     print(r.text)


# 事件钩子
def print_url(r, *args, **kwargs):
    print(type(r), r.url)
    raise RuntimeError("requests hook runtime error")

# with requests.Session() as s:
#     r = s.get("https://httpbin.org/get", hooks={"response": print_url})
#     print(r.text)


# 自定义身份验证
# HTTPBasicAuth
# HTTPDigestAuth


# 流式请求
# with requests.Session() as s:
#     r = s.get("https://httpbin.org/stream/20", stream=True)
#     if not r.encoding:
#         r.encoding = "utf-8"
#
#     # for chunk in r.iter_content(chunk_size, decode_unicode=True):
#     for line in r.iter_lines(decode_unicode=True):
#         if line:
#             print(json.loads(line))


# 代理
proxies = {
    "http": "http://user:pass@10.10.1.10:3128", # 代理需要 HTTP Basic Auth
    "https": "http://10.10.1.10:1080",
    "http://10.20.1.128": "http://10.10.1.10:5323"  # 为某个特性的连接设置代理
}
# 配置单个请求
# requests.get("http://example.org", proxies=proxies)
# 配置所有请求, 配置环境变量
# export HTTP_PROXY="http://10.10.1.10:3128"
# export HTTPS_PROXY="http://10.10.1.10:1080"
# requests.get("http://example.org")

# SOCKS 代理
# pip install socks
proxies = {
    'http': 'socks5://user:pass@host:port',
    'https': 'socks5://user:pass@host:port'
}


