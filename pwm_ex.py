import machine
from machine import Pin

# PWM settings
pwm0 = machine.PWM(Pin(0), freq=20000000, duty_u16=32768)

while 1:
    # a = float(input())
    # a = a / 65536
    # pwm0.duty_u16(a)

    print(f"input frequency settings")
    freq = int(input())
    print(f"frequency set to {freq}")
    pwm0.freq(freq)
