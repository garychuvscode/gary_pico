import machine
import utime
import time
import rp2
import _thread
from machine import Pin

# fmt: off

# 初始化USB串口
usb_cdc = machine.UART(0, baudrate=115200)

# 初始化UART1串口
uart1 = machine.UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))  # 替换Pin(4)和Pin(5)为实际的引脚
led = machine.Pin(25, machine.Pin.OUT)

# 线程函数1
def thread1():
    while True:
        print("Thread 1 is running")
        time.sleep(1)


# 启动线程1
_thread.start_new_thread(thread1, ())

# 主线程
while True:
    # 在这里可以执行其他任务
    led.value(1)
    time.sleep(0.3)
    led.value(0)
    time.sleep(0.3)
    led.value(1)
    time.sleep(0.3)
    led.value(0)
    time.sleep(0.3)
    print("Main Thread is running")
    pass
