# fmt: off


import machine
import utime
import time
import rp2
from machine import Pin

# this lib can't be used in micropython
# # this import is used for the string TAB adjustment
# import textwrap

"""

this will be the main program operated automatically after PICO powered up
only used for main program development

"""

# default frequency 150MHz
f_now = machine.freq()
print(f"requency now is: {f_now}")
machine.freq(250000000)
print(machine.freq())

led1 = machine.Pin(0, machine.Pin.OUT)


while 1 :
    led1.value(0)
    led1.value(1)
