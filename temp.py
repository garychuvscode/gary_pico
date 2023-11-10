import rp2
from machine import Pin
import machine
import time

io = machine.Pin(8, machine.Pin.OUT)
# 设置 x 寄存器的初始值
x_value = 3


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    pass


sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(8))
sm.active(1)
sm.exec("set(pins, 1)[0]")
sm.exec("set(pins, 0)[0]")


# @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, autopull=True, autopush=True)
# def generate_pulse():
#     set(x, 3)  # 设置 x 寄存器的值
#     label("start")
#     set(pins, 1)[0]
#     set(pins, 0)[0]
#     nop()[31]
#     nop()[31]
#     nop()[31]
#     nop()[31]
#     jmp(x_dec, "start")  # 跳转到 "start" 标签，当 x 寄存器递减到零时停止循环
#     jmp("done")
#     label("done")
#     pass


# # 初始化計數器
# irq_count = 0


# # 创建状态机并启动
# sm = rp2.StateMachine(0, generate_pulse, freq=10000000, set_base=Pin(8))
# sm.active(1)
# time.sleep(1)
# sm.active(0)


# while True:
#     sm.exec("set(pins, 1)")
#     sm.exec("set(pins, 0)")
#     time.sleep(10000)

# exec("irq_count = irq_count + 1")
# exec("if irq_count == 50:")
# exec("if irq_count == 50")
# jmp("start")
