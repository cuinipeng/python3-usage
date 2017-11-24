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
from multiprocessing import freeze_support

queue_size = 1024
port = 20000
authkey = b'123456789'

def posix_run():
    # 1. 建立 task_queue 和 result_queue
    task_queue = queue.Queue(maxsize=queue_size)
    result_queue = queue.Queue(maxsize=queue_size)

    class QueueManager(BaseManager):
        pass

    # 2. 注册创建的队列, callable 关联了 Queue 对象
    QueueManager.register('get_task_queue', callable=lambda: task_queue)
    QueueManager.register('get_result_queue', callable=lambda: result_queue)

    # 3. 绑定端口 8080, 设置认证口令
    manager = QueueManager(address=('', port), authkey=authkey)

    try:
        # 4. 启动管理, 监听信息通道
        manager.start()

        # 5. 通过管理实例的方法获得通过网络访问的 Queue 对象
        task  = manager.get_task_queue()
        result = manager.get_result_queue()

        # 6. 添加任务
        urls = ['https://www.csdn.net/', 'https://www.baidu.com/', 'https://www.zhihu.com/']
        for url in urls:
            print('[%s] put task %s to queue ...' % (os.getpid(), url))
            task.put(url, block=True, timeout=None)

        # 7. 获取任务结果
        print('[%s] try get result ...' % os.getpid())
        for i in range(16):
            print('[%s] result is %s' % (os.getpid(), result.get(timeout=10)))
    except Exception as e:
        print(e)
    finally:
        # 8. 关闭管理
        manager.shutdown()


def win_run():
    # Windows 10 + Python 3.6.3 验证有问题
    """
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "D:\Program Files\Python36\lib\multiprocessing\spawn.py", line 99, in spawn_main
        new_handle = reduction.steal_handle(parent_pid, pipe_handle)
      File "D:\Program Files\Python36\lib\multiprocessing\reduction.py", line 82, in steal_handle
        _winapi.PROCESS_DUP_HANDLE, False, source_pid)
    OSError: [WinError 87] 参数错误。
    """
    # 1. 建立 task_queue 和 result_queue
    task_queue = queue.Queue(maxsize=1024)
    result_queue = queue.Queue(maxsize=1024)

    class QueueManager(BaseManager):
        pass

    def get_task_queue():
        return task_queue

    def get_result_queue():
        return result_queue

    # 2. 注册创建的队列, callable 关联了 Queue 对象
    #    Windows 调用接口不能使用 lambda, 所以先定义函数在绑定
    QueueManager.register('get_task_queue', callable=get_task_queue)
    QueueManager.register('get_result_queue', callable=get_result_queue)

    # 3. 绑定端口 8080, 设置认证口令
    #    Windows 需要显式指定 IP 地址
    manager = QueueManager(address=('127.0.0.1', port), authkey=authkey)

    try:
        # 4. 启动管理, 监听信息通道
        manager.start()

        # 5. 通过管理实例的方法获得通过网络访问的 Queue 对象
        task  = manager.get_task_queue()
        result = manager.get_result_queue()

        # 6. 添加任务
        urls = ['https://www.csdn.net/', 'https://www.baidu.com/', 'https://www.zhihu.com/']
        for url in urls:
            print('[%s] put task %s to queue ...' % (os.getpid(), url))
            task.put(url, block=True, timeout=None)

        # 7. 获取任务结果
        print('[%s] try get result ...' % os.getpid())
        for i in range(16):
            print('[%s] result is %s' % (os.getpid(), result.get(timeout=10)))
    except Exception as e:
        print(e)
    finally:
        # 8. 关闭管理
        manager.shutdown()


if __name__ == '__main__':
    if os.name == 'nt':
        freeze_support()
        win_run()
    elif os.name == 'posix':
        posix_run()
