import rp2
from machine import Pin
import machine
import time

led = machine.Pin(1, machine.Pin.OUT)
io = machine.Pin(8, machine.Pin.OUT)
io.value(0)
time.sleep(0.2)

# 将系统时钟频率设置为 250 MHz
machine.freq(250000000)
# 获取当前系统时钟频率
current_freq = machine.freq()
print("Current frequency:", current_freq)

ts_pin = machine.Pin(8, machine.Pin.OUT)


cmd = """

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def led_blink():
    # set(pins, 1)[0]
    # set(pins, 0)[0]
    # set(pins, 1)[0]
    label("mainloop")
    pull(noblock)  # Loads OSR with delay value
    mov(x, osr)  # OSR contents to X to prepare for future noblock pulls
    # set(x, 10)

    label("pulse_s")
    # label("delay_on")
    set(pins, 1)[0]
    set(pins, 1)[0]
    set(pins, 1)[0]
    set(pins, 1)[0]
    set(pins, 1)[0]
    # jmp(x_dec, "delay_on")[0]
    # nop()[31]
    # label("delay_off")
    set(pins, 0)[0]
    set(pins, 0)[0]
    set(pins, 0)[0]
    set(pins, 0)[0]
    # jmp(y_dec, "delay_off")[0]
    jmp(x_dec, "pulse_s")[0]
    label("end_p")  # Start of on timer
    set(pins, 0)[0]  # pattern end
    jmp("end_p")  # Jumps to the beginning of the blink routine


sm1 = rp2.StateMachine(
    1, led_blink, freq=250000000, set_base=Pin(8)
)  # Instantiates State Machine 1
sm1.put(4)
sm1.active(1)  # Starts State Machine 1

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
str_to_code(cmd)
str_to_code(cmd)
str_to_code(cmd)
