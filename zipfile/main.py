#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import zlib
import zipfile

#
# unzip -l archive-1.0.zip
# unzip archive-1.0.zip -d ./tmp
#

files = ["data/data-1.txt", "data/data-2.txt", "data/data-3.txt"]
zfname = "archive-1.0.zip"
z = zipfile.ZipFile(zfname, "w", zipfile.ZIP_DEFLATED)

for f in files:
    if os.path.exists(f):
        z.write(f)

print(z.namelist())
print(z.extract("data/data-1.txt", "tmp"))
z.close()


