#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# CPU 密集型建议使用多进程
# IO 密集型建议使用多线程, 比如爬虫,大部分时间等待 Socket IO
#
# Python 协程支持, gevent 是一个基于协程的 Python 网络函数库,
# 使用基于 greenlet 在 libev 事件循环顶部提供了一个有高级别
# 并发行的 API:
# http://www.gevent.org/contents.html
#   1. 基于 libev 的快速事件循环, Linux 上是 epoll 机制
#   2. 基于 greentlet 的轻量级执行单元
#   3. API 复用了 Python 标准库的内容
#   4. 支持 SSL 的协作式 sockets
#   5. 可通过线程池或 c-ares 实现 DNS 查询
#   6. 通过 monkey patch 功能使得第三方模块变成协作式
#
# 在 CPU 的角度来说, 协程就是单线程,省去上下文切换开销
#
# 在做多进程或多线程测试时, 应该关闭 monkey.patch_all()
# 
from gevent import monkey; monkey.patch_all()
import gevent, gevent.pool
import threading
import os, uuid, time, random, urllib, urllib.request
from multiprocessing import Process, Pool, Queue, Pipe

# 子进程执行的代码
def run_task(name):
    print('[%s] Task %s is running...' % (os.getpid(), name))
    time.sleep(random.random() * 3)
    print('[%s] Task %s end' % (os.getpid(), name))


def create_multi_process():
    print('[%s] Current process start' % os.getpid())

    processes = []
    for i in range(5):
        process = Process(target=run_task, args=[str(uuid.uuid4())])
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    print('[%s] All subprocesses end' % os.getpid())


def create_process_pool():
    print('[%s] Current process start' % os.getpid())

    # 当进程池中线程达到最大值时,新的进程就会等待,会复用先前创建的进程
    pool = Pool(processes=3)
    for i in range(5):
        pool.apply_async(run_task, args=[str(uuid.uuid4())])

    pool.close()
    pool.join()
    print('[%s] All subprocesses end' % os.getpid())


# 进程间通信
def proc_reader(q):
    print('[%s] reading...' % os.getpid())
    while True:
        url = q.get(block=True, timeout=None)
        print('[%s] get %s from queue' % (os.getpid(), url))


def proc_writer(q, urls):
    print('[%s] writing...' % os.getpid())
    for url in urls:
        q.put(url, block=True, timeout=None)
        print('[%s] put %s to queue' % (os.getpid(), url))
        time.sleep(random.random() * 3)


def multi_process_communicate_by_queue():
    q = Queue()
    urls_1 = ['https://amazom.com', 'https://google.com', 'https://youtube.com']
    urls_2 = ['https://www.csdn.net', 'https://baidu.com', 'https://163.com']
    reader = Process(target=proc_reader, args=[q])
    writer_1 = Process(target=proc_writer, args=[q, urls_1])
    writer_2 = Process(target=proc_writer, args=[q, urls_2])
    reader.start()
    writer_1.start()
    writer_2.start()
    writer_1.join()
    writer_2.join()
    reader.terminate()


# 多线程操作
g_num = 0
g_lock = threading.RLock()
class TaskThread(threading.Thread):
    def __init__(self, name):
        super().__init__(name=name)
        # threading.Thread.__init__(self, name=name)

    def run(self):
        global g_num
        while True:
            g_lock.acquire()
            print('[*] %s get lock at num %d' % (threading.current_thread().name, g_num))
            if g_num >= 4:
                g_lock.release()
                print('[*] %s release lock at num %d' % (threading.current_thread().name, g_num))
                break
            g_num += 1
            g_lock.release()
            print('[*] %s release lock at num %d' % (threading.current_thread().name, g_num))
            time.sleep(random.random())


def crate_multi_thread():
    t1 = TaskThread(str(uuid.uuid4()))
    t2 = TaskThread(str(uuid.uuid4()))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


# 协程 API
# 基于 gevent.spawn 和 gevent.joinall 示例
def run_greenlet_task(url):
    print('==> visit %s' % url)
    try:
        r = urllib.request.urlopen(url, timeout=2)
        data = r.read()
        length = r.headers.get('Content-Length')
        print('%d(%s) received from %s' % (len(data), length, url))
    except Exception as e:
        return {'status': 1}

    return {'status': 0}


def create_greenlet():
    urls = ['https://www.csdn.net/', 'https://www.baidu.com/', 'https://www.zhhu.com/']
    greenlets = [gevent.spawn(run_greenlet_task, url) for url in urls]
    gevent.joinall(greenlets)


def create_greenlet_pool():
    # 当协程池满的时候,新添加的协程会等待
    pool = gevent.pool.Pool(2)
    urls = ['https://www.csdn.net/', 'https://www.baidu.com/', 'https://www.zhihu.com/']
    results = pool.map(run_greenlet_task, urls)
    print(results)

if __name__ == '__main__':
    # create_multi_process()
    # create_process_pool()
    # multi_process_communicate_by_queue()
    # crate_multi_thread()
    # create_greenlet()
    create_greenlet_pool()
