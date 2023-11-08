import machine
from machine import Pin

# PWM settings
pwm0 = machine.PWM(Pin(0), freq=25000000, duty_u16=32765)

while 1:
    # a = float(input())
    # a = a / 65536
    # pwm0.duty_u16(a)

    # print(f"input frequency settings")
    # freq = int(input())
    # print(f"frequency set to {freq}")
    # pwm0.freq(freq)

    print(
        f"input duty settings is {pwm0.duty_u16()}, /65535 is {float(pwm0.duty_u16())/65535} and % is {int(float(pwm0.duty_u16())/65535*100)}"
    )
    print(
        f"pwm_d is {pwm0.duty_u16()}, result is {float(pwm0.duty_u16())/65535}, percentage: {pwm0.duty_u16()/65535*100}"
    )
    a = input()
    b = float(a) / 100
    c = b * 65535

    duty = int(c)
    print(f"duty set to {duty}, with {a}%, {b} after / 100, {c} is the result")
    pwm0.duty_u16(duty)
