import rp2
from machine import Pin
import machine
import time

led = machine.Pin(25, machine.Pin.OUT)
io = machine.Pin(8, machine.Pin.OUT)
io.value(0)
time.sleep(0.2)


@rp2.asm_pio()
def loop_with_count():
    set(pins, 1)  # Set the pins high
    mov(x, 10)  # Set the high count
    label("high_loop")
    jmp(x_dec, "high_loop")  # Decrement x and jump if not zero
    set(pins, 0)  # Set the pins low
    mov(x, 5)  # Set the low count
    label("low_loop")
    jmp(x_dec, "low_loop")  # Decrement x and jump if not zero
    jmp("high_loop")  # Jump back to the high loop


# 创建PIO状态机
sm = rp2.StateMachine(0, loop_with_count, freq=100000, set_base=Pin(8))

# 启动PIO程序
sm.active(1)

# 等待一段时间后停止PIO程序
time.sleep(2)
sm.active(0)
