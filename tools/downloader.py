#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import requests
from urllib.parse import urlsplit

def download(url, chunk_size=8192 * 4, timeout=5):
    
    sr = urlsplit(url)
    host = sr.netloc
    filename = os.path.basename(sr.path)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Host": host
    }

    with requests.Session() as s:
        s.headers.update(headers)
        # print(json.dumps(dict(s.headers), indent=2))
        r = s.get(url, stream=True, timeout=timeout)
        print("Downlading {0}".format(filename))
        print("Content-Type: {0}".format(r.headers["Content-Type"]))
        print("Content-Length: {0} Byte".format(r.headers["Content-Length"]))
        with open(filename, "wb") as fd:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)
                print(".", end="", flush=True)

        print("\nDownload {0}".format(filename))


if __name__ == "__main__":
    download("http://mirror.bit.edu.cn/apache/spark/spark-2.2.0/spark-2.2.0-bin-hadoop2.7.tgz")
