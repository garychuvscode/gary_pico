import machine
import test as t
import time

test_o = t.test_obj()


# 定义定时器中断处理函数
def timer_callback(timer):
    # print("Timer expired, toggle IO")
    test_o.toggle_once()


# 创建一个定时器对象，周期为1毫秒
timer = machine.Timer(freq=1000)
timer.init(mode=machine.Timer.PERIODIC, period=10, callback=timer_callback)

# 运行无限循环以保持程序运行
while 1:
    pass


# x = 0
# while x < 6:
#     x = x + 1
#     time.sleep(5)
#     pass
