import rp2
from machine import Pin
import machine
import time

led = machine.Pin(1, machine.Pin.OUT)


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    # wrap_target()
    set(pins, 1)[0]
    set(pins, 0)[0]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]

    # wrap()


def str_to_code(string0=""):
    string0 = str(string0)
    exec(string0)


"""
pattern gen need:
1. pulse out => high or low (glitch testing)
2. random pattern
3. SWIRE pulse (low pulse)
"""


sm = rp2.StateMachine(0, blink, freq=10000000, set_base=Pin(0))
# led.value(1)
sm.active(1)
sm.active(0)  # 停止PIO程序
# led.value(0)


# minimum delay needed for single minimum pulse

# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]
# nop()[31]

# 231109 need to test this function, but add the
# length of pattern to enough amount
# # 等待PIO程序完成一次执行
# while not sm.irq().irq0:
#     pass

"""
coding note:

convert code from string:

# the one with return value
code_string = "3 + 4"
result = eval(code_string)
print(result)  # 输出 7
#

# the one without return
code_string = "print('Hello, world!')"
exec(code_string)  # 输出 "Hello, world!"
#



"""
