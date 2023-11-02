import machine
import utime
import time
import rp2
import _thread
from machine import Pin

import os

# fmt: off
"""

this will be the main program operated automatically after PICO powered up
only used for main program development

"""

# default frequency 150MHz
f_now = machine.freq()
print(f"requency now is: {f_now}")


# 初始化USB串口
usb_cdc = machine.UART(0, baudrate=115200)

# 初始化UART1串口
uart1 = machine.UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))  # 替换Pin(4)和Pin(5)为实际的引脚
led = machine.Pin(25, machine.Pin.OUT)

# 0 is simulation mode, 1 is real mode
sim_mode = 0


def msg_output(counter0 = 0, output_set0=0, msg_content0='', direct_send=0):
    '''
    print message based on the output_set in infinite loop
    '''
    if counter0 % output_set0 == 0  or direct_send == 1 :
        print(f'{msg_content0}')

# 线程函数1
def thread1():
    # counter for infinite loop, for skipping flag indication
    x_count = 0
    output_set = 500
    # thread1 is used to checking the UART bus, if there are data input
    while True:

        msg_temp = f'now is checking the UART port from USB'
        msg_output(counter0=x_count, output_set0=200, msg_content0=msg_temp)

        if sim_mode == 1 :
            # for the real mode, check the UART input bus from the USB port

            if usb_cdc.any() :
                data = usb_cdc.read(64)  # 读取USB串口的数据
                # 在这里可以处理接收到的数据
                # 例如，你可以回传收到的数据
                usb_cdc.write(data)
                led.value(1)
                time.sleep(4)
                led.value(0)
                time.sleep(4)
                led.value(1)
                time.sleep(4)
                led.value(0)
                time.sleep(4)
                print(f"get the UART input: {data}")
                pass

            pass
        else:

            msg_temp = f'finished the UART input'
            msg_output(counter0=x_count, output_set0=500, msg_content0=msg_temp)
            # time.sleep_ms(250)

        x_count = x_count + 1

        if x_count == 5000 :
            # reset counter
            x_count = 0

        # end while
        pass

    # end thread
    pass




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

# # able to use this method and COM port open
# while True:
#     led.value(1)
#     time.sleep(0.3)
#     led.value(0)
#     time.sleep(0.3)
#     led.value(1)
#     time.sleep(0.3)
#     led.value(0)
#     time.sleep(0.3)

#     if usb_cdc.any():
#         data = usb_cdc.read(64)  # 读取USB串口的数据
#         # 在这里可以处理接收到的数据
#         # 例如，你可以回传收到的数据
#         usb_cdc.write(data)
#         led.value(1)
#         time.sleep(10)
#         led.value(0)
#         time.sleep(10)
#         pass

#     # led.value(1)
#     # time.sleep(0.3)
#     # led.value(0)
#     # time.sleep(0.3)


# # method 2
# import machine
# import os

# # 初始化USB串口
# usb_cdc = machine.UART(0, baudrate=115200)

# while True:
#     if usb_cdc.any():
#         data = usb_cdc.read(64)  # 读取USB串口的数据
#         # 在这里可以处理接收到的数据
#         # 例如，你可以回传收到的数据
#         usb_cdc.write(data)

# # method 1
# # 通过USB创建虚拟串口
# uart = machine.UART(0, baudrate=115200)

# while True:
#     # 从串口接收数据
#     data = uart.read(64)  # 读取最多64字节的数据

#     if data:
#         # 处理接收到的数据
#         # 在这里可以执行与查询相关的操作
#         input_data = data.decode('utf-8')
#         response = "Received: " + data.decode('utf-8')
#         uart.write(response)
#         print(f'the received message is:{response}')

#     time.sleep(0.1)  # 稍微延迟以允许其他操作
