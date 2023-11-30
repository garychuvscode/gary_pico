# Example of using PIO writing a parallel byte from data
# for a more wrapped-up examples, see https://github.com/raspberrypi/pico-micropython-examples/blob/master/pio/pio_pwm.py

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep
import rp2
import machine

# 将系统时钟频率设置为 250 MHz
machine.freq(250000000)
# 获取当前系统时钟频率
current_freq = machine.freq()
print("Current frequency:", current_freq)


@asm_pio(
    out_init=(rp2.PIO.OUT_HIGH,) * 8,
    out_shiftdir=PIO.SHIFT_RIGHT,
    autopull=True,
    pull_thresh=8,
)
def paral_prog():
    pull()
    out(pins, 8)
    pass


paral_sm = StateMachine(0, paral_prog, freq=20000000, out_base=Pin(0))
paral_sm.active(1)

for i in range(65536):
    # print(i)
    paral_sm.put(i)
    """
    put the binary index to the shift register, overflow is also
    ok, original sample is set to 500

    """
    print(i)
    # sleep(0.01)
