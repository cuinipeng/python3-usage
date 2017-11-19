#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import time
from ctypes import *

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():
    
    # 获得前台窗口的句柄
    hwnd = user32.GetForegroundWindow()

    # 获得进程 ID
    pid = c_long(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # 保存当前进程的 ID
    process_id = "%d" % pid.value

    # 申请内存
    executable = create_string_buffer(512)

    # 打开进程
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    # 可执行文件名字
    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    # 读取窗口标题
    window_title = create_string_buffer(512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)

    print("[PID: %s - %s - %s]" % (process_id, executable.value, window_title.value))

    # 关闭句柄
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    

if __name__ == "__main__":
    get_current_process()
