#!/usr/bin/env python3
#
# nat_start_time|nat_end_time|public_ip|public_port|private_ip|private_port|user_agent|target_server|target_port|content_length
#
# http://tech.glowing.com/cn/dealing-with-timezone-in-python/
#
import IPy
import os
import uuid
import time
import pytz
import random
import datetime

hosts = ["baidu.com", "google.com", "stackoverflow.com", "github.com",
    "csnd.net", "youtube.com", "oschina.net", "jd.com", "tmall.com"]
host_ports = [21, 22, 80, 443]
user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"]
public_ips = ["10.10.10.10"]
private_ips = [str(ip) for ip in IPy.IP("192.168.13.0/24")]

rand = random.SystemRandom()
# Choose a random element from a non-empty sequence.
host = rand.choice(hosts)
# Return random integer in range [a, b], including both end points.
port = rand.randint(30, 30000)

# Current local datetime, <class 'datetime.datetime'>
now = datetime.datetime.now()
# UTC datetime, <class 'datetime.datetime'>
utcnow = datetime.datetime.utcnow()
utcnow = datetime.datetime.now(pytz.utc)
utcnow = datetime.datetime.now(pytz.timezone("UTC"))
timedelta = datetime.timedelta(days=1, seconds=90, microseconds=0000)
total = utcnow + timedelta
fmtnow = utcnow.strftime("%Y-%m-%d %H:%M:%S")

# print(utcnow)
# print(timedelta)
# print(timedelta.total_seconds())
# print(total)
# print(fmtnow)

# nat_start_time|nat_end_time|public_ip|public_port|private_ip|private_port|user_agent|target_server|target_port|content_length
# 构造时间乱序的数据
# 起始时间为当前时间戳加上 [0, 86400] 的随机增量
# 结束时间为起始时间加上 [5, 30] 的随机增量
def generate_one_data():
    nat_start_time = datetime.datetime.utcfromtimestamp(time.time() + rand.randint(0, 24 * 60 * 60))
    nat_end_time = nat_start_time + datetime.timedelta(seconds=rand.randint(5, 30))
    nat_start_time = nat_start_time.strftime("%Y-%m-%d %H:%M:%S")
    nat_end_time = nat_end_time.strftime("%Y-%m-%d %H:%M:%S")
    # print(nat_start_time, '->', nat_end_time)

    public_ip = rand.choice(public_ips)
    public_port = str(rand.randint(1, 65535))
    private_ip = rand.choice(private_ips)
    private_port = str(rand.randint(1024, 65535))
    user_agent = rand.choice(user_agents)
    target_server = rand.choice(hosts)
    target_port = str(rand.choice(host_ports))
    content_length = str(rand.randint(800, 5000))

    data = [nat_end_time, nat_end_time, public_ip, public_port, private_ip, private_port, user_agent, target_server, target_port, content_length]
    data = "|".join(data)
    
    return data

def generate_data(length=100):
    if not os.path.exists("data"):
        os.makedirs("data")
    
    filename = str(uuid.uuid4()).replace("-", "").upper() + ".txt"
    fullpath = os.path.join("data", filename)
    with open(fullpath, "wb") as out:
        for i in range(length):
            if i == (length - 1):
                out.write(bytes(generate_one_data(), encoding="utf-8"))
            else:
                out.write(bytes(generate_one_data() + "\n", encoding="utf-8"))

    print("generate {0} length data at {1}".format(length, fullpath))

if __name__ == "__main__":
    for i in range(1):
        generate_data(10000)
    pass
