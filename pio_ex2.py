import rp2
from machine import Pin
import machine
import time

led = machine.Pin(1, machine.Pin.OUT)
io = machine.Pin(8, machine.Pin.OUT)
io.value(0)
time.sleep(0.2)

cmd = """
io.value(0)
time.sleep(0.2)
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def loop_with_count():
    set(pins, 1)   # Set the pins high
    mov(x, 10)     # Set the high count
    label("high_loop")
    jmp(x_dec, "high_loop")  # Decrement x and jump if not zero
    set(pins, 0)   # Set the pins low
    mov(x, 5)      # Set the low count
    label("low_loop")
    jmp(x_dec, "low_loop")   # Decrement x and jump if not zero
    jmp("high_loop")  # Jump back to the high loop

sm = rp2.StateMachine(0, loop_with_count, freq=10000000, set_base=Pin(8))
sm.active(1)
time.sleep(0.05)
sm.active(0)

"""


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
