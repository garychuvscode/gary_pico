import rp2
from machine import Pin
import machine
import time

led = machine.Pin(25, machine.Pin.OUT)
io = machine.Pin(8, machine.Pin.OUT)
io.value(0)
time.sleep(0.5)

# io.value(1)
# # time.sleep(0.01)
# io.value(0)


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    pull(noblock)  # Loads OSR with delay value
    # mov(x, osr)  # OSR contents to X to prepare for future noblock pulls
    # mov(y, x)
    # mov(x, 10)  # Set the high duration
    set(pins, 1)[0]  # Set the pins high
    set(pins, 0)[0]
    label("pos_d")
    set(pins, 1)[0]
    jmp(x_dec, "pos_d")[0]  # Decrement x and jump if not zero

    mov(y, 5)  # Set the low duration
    set(pins, 0)[0]  # Set the pins low
    label("neg_d")
    jmp(y_dec, "neg_d")[0]  # Decrement x and jump if not zero


# 创建PIO状态机
sm = rp2.StateMachine(0, blink, freq=250000000, set_base=Pin(8))

# 启动PIO程序
sm.active(1)

# sm.put(15)

# 等待一段时间后停止PIO程序
time.sleep(0.1)
sm.active(0)

"""

nop()[31]
set(pins, 1)[0]  # Set the pins high
mov(x, 10)  # Set the high count
label("high_loop")
set(pins, 1)[0]  # Set the pins high
set(pins, 0)[0]  # Set the pins low
jmp(x_dec, "high_loop")  # Decrement x and jump if not zero
set(pins, 0)  # Set the pins low
mov(x, 5)  # Set the low count
label("low_loop")
jmp(x_dec, "low_loop")  # Decrement x and jump if not zero
jmp("high_loop")  # Jump back to the high loop

"""
