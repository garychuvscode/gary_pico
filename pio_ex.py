import rp2
from machine import Pin
import machine
import time

led = machine.Pin(1, machine.Pin.OUT)
io = machine.Pin(8, machine.Pin.OUT)
io.value(0)
time.sleep(0.2)
# @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
# def blink():
#     # wrap_target()
#     set(pins, 1)[0]
#     set(pins, 0)[0]
#     nop()[31]
#     nop()[31]
#     nop()[31]
#     nop()[31]

cmd = """
# io.value(0)
# time.sleep(0.2)
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    set(pins, 1)[0]
    set(pins, 0)[0]
    label("done")
    jmp("done")


sm = rp2.StateMachine(0, blink, freq=10000000, set_base=Pin(8))
sm.active(1)
# time.sleep(0.05)
# sm.active(0)

"""

print(cmd)

# # machine.soft_reset(machines=[machine.SOFT_RESET_PIO0])
# while True:
#     data = sm.get()  # 从 FIFO 读取数据，但忽略它
#     if data == -1:  # 当 FIFO 为空时，退出循环
#         break


def str_to_code(string0=""):
    # string0 = str(string0)
    exec(string0)


"""
pattern gen need:
1. pulse out => high or low (glitch testing)
2. random pattern
3. SWIRE pulse (low pulse)
"""
# cmd = "print(f'hello')"

# sm = rp2.StateMachine(0, blink, freq=10000000, set_base=Pin(0))
# # led.value(1)
# sm.active(1)
# sm.active(0)  # 停止PIO程序
# led.value(0)

str_to_code(cmd)


"""
this eaxmple use python to process asm_pio, not suggest to use
delay too long.. (6ms)

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    pass
sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(8))
sm.active(1)
sm.exec("set(pins, 1)[0]")
sm.exec("set(pins, 0)[0]")

"""
