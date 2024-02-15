import machine
from machine import Pin
import time 

# 将引脚设置为默认上拉
button = Pin(24, Pin.IN, Pin.PULL_UP)

while 1 : 

    print(f'the button now is: {button.value()}')
    time.sleep(0.7)
