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
# print(f"requency now is: {f_now}")
machine.freq(250000000)
# print(machine.freq())



# 0 is simulation mode (work with teriminal, or USB COM)=> print all
# 1 is real mode (use real interface read and write) => only for return message
# 2 is real debug mode, need to check termainal print =>
sim_mode = 2


class pico_emb():

    def __init__(self, sim_mcu0=0):

        # ===== input command
        self.cmd_array = []

        self.str_cmd =''

        self.sim_mcu = sim_mcu0

        # simulation mode temp space
        self.sim_args = []
        self.sim_kwargs = []

        # ===== the only LDE on PICO, reserve for LED
        self.led = machine.Pin(25, machine.Pin.OUT)

    def led_toggle(self, duration=0.1):
        '''
        LED toggle function, once receive command toggle,
        and duration is changeable, based on special command
        '''
        self.led.value(1)
        utime.sleep(duration)
        self.led.value(0)
        utime.sleep(duration)
        pass

    def pico_emb_main(self):
        pwr_signal = 0
        while 1 :

            if pwr_signal == 0 :
                # power up before wait command, toggle LED for PWR up
                self.led_toggle(duration=0.3)
                self.led_toggle(duration=0.3)
                self.led_toggle(duration=0.3)
                pwr_signal = 1

                pass

            print(f'end of testing, ok to off, print all input ')
            x = input()
            print(f'repeat: {x}')


pico_grace= pico_emb(sim_mcu0=sim_mode)
# pico_grace.pico_emb_main()
# pico_grace.debug_led(num0=1, value0=1, all=1)

# pico_grace.pico_emb_main()
