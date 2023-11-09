import rp2
from machine import Pin
import machine
import time

led = machine.Pin(1, machine.Pin.OUT)


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    # wrap_target()
    set(pins, 1)[0]
    # nop()[31]
    # nop()[31]
    # nop()[31]
    # nop()[31]
    set(pins, 0)[0]
    # nop()[31]
    # nop()[31]
    # nop()[31]
    # nop()[31]

    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]

    # wrap()


sm = rp2.StateMachine(0, blink, freq=10000000, set_base=Pin(0))
led.value(1)
sm.active(1)

# 231109 need to test this function, but add the
# length of pattern to enough amount
# # 等待PIO程序完成一次执行
# while not sm.irq().irq0:
#     pass

sm.active(0)  # 停止PIO程序
led.value(0)
