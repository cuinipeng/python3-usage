#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

filename = "example.csv"

with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    row = ["Spam"] * 5 + ["Baked Beans"] + ["Hello,World"]
    rows = [row for i in range(3)]
    writer.writerow(row)
    writer.writerows(rows)

with open(filename, "r", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        print(row, type(row))


with open(filename, "w", newline="") as csvfile:
    fieldnames = ["first_name", "last_name"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    row = {
        "first_name": "Percy",
        "last_name": "Cui"
    }
    rows = [row for i in range(3)]
    writer.writerow(row)
    writer.writerows(rows)

with open(filename, "r", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row, type(row), reader.line_num)
