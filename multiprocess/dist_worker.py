#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 分布式进程指的是将 Process 进程分布到多台机器.
#
# multiprocessing 模块支持在多台机器上运行管理多进程,
# 举例来说, 就是一个服务管理进程作为调度者, 将任务分
# 发到多个进程中, 依靠网络通信进行管理. 在爬虫程序中,
# 一个进程负责抓取图片连接, 将连接放在队列中, 另外的
# 机器负责下载. 问题是如何将 Queue 暴露在网络,在多个
# 分布式进程之间共享, 这个过程称之为本地队列网络化.
#
import random, time, queue, os
from multiprocessing.managers import BaseManager

server_host = '127.0.0.1'
server_port = 20000
authkey = b'123456789'

class QueueManager(BaseManager):
    pass

# 1. 注册用于获取 Queue 的名称和方法
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')


try:
    # 2. 连接到服务器
    print('[*] connect or server %s:%d' % (server_host, server_port))
    manager = QueueManager(address=(server_host, server_port), authkey=authkey)
    manager.connect()

    # 3. 获取 Queue 对象
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    # 4. 从 task 队列获取任务, 并将结果写入 result 队列
    while not task.empty():
        url = task.get(block=True, timeout=5)
        print('[%d] run task download %s...' % (os.getpid(), url))
        time.sleep(1)
        print('[%d] upload task result...' % os.getpid())
        result.put('%s --> success' % url, block=True, timeout=5)
except Exception as e:
    print(e)
# finally:
#     只有当 manager 作为 server 端监听时才有 shutdown 接口,
#     作为 客户端连接是没有shutdown 接口的
#     manager.shutdown()

