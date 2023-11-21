from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
import machine
import time

# 将系统时钟频率设置为 250 MHz
machine.freq(250000000)
# 获取当前系统时钟频率
current_freq = machine.freq()
print("Current frequency:", current_freq)

led = machine.Pin(25, machine.Pin.OUT)
ts_pin = machine.Pin(8, machine.Pin.OUT)


@asm_pio(set_init=PIO.OUT_LOW)
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


sm1 = StateMachine(
    1, led_blink, freq=250000000, set_base=Pin(8)
)  # Instantiates State Machine 1
sm1.put(4)
sm1.active(1)  # Starts State Machine 1
time.sleep(0.1)
sm1.active(0)

while True:
    value = int(input("enter delay:")) - 1
    sm1.put(value)  # Output the next Byte
    sm1.active(1)  # Starts State Machine 1
    time.sleep(0.1)
    # sm1.active(0)
    # sm1.restart()
    print(value)
