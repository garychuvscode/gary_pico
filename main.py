# fmt: off


import machine
import utime
import time
import rp2
from machine import Pin


"""

this will be the main program operated automatically after PICO powered up
only used for main program development

"""

# default frequency 150MHz
f_now = machine.freq()
# print(f"requency now is: {f_now}")

# 0 is simulation mode (work with teriminal, or USB COM),
# 1 is real mode (use real interface read and write)
sim_mode = 1

class pico_emb():

    def __init__(self, sim_mcu0=0):


        self.cmd_array = []

        self.sim_mcu = sim_mcu0
        self.baud_r_com = 9600

        self.led = machine.Pin(25, machine.Pin.OUT)
        self.uart1 = machine.UART(1, baudrate=self.baud_r_com, tx=Pin(4), rx=Pin(5))  # 替换Pin(4)和Pin(5)为实际的引脚

        # PWM settings
        pwm0 = machine.PWM(Pin(0), freq=2000, duty_u16=32768)

        # debug led settings
        self.led1 = machine.Pin(1, machine.Pin.OUT)
        self.led2 = machine.Pin(9, machine.Pin.OUT)
        self.led3 = machine.Pin(13, machine.Pin.OUT)
        self.led4 = machine.Pin(18, machine.Pin.OUT)
        self.led5 = machine.Pin(22, machine.Pin.OUT)

        # reset all the LED
        self.debug_led(num0=1, value0=0, all=1)

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

    def debug_led(self, num0=1, value0=1, all=0):
        '''
        num0 = 1 to 5
        value0 = 0 or 1
        all = 0 or 1
        '''

        if all == 0:
            # single change
            if num0 == 1:
                self.led1.value(value0)
                pass
            elif num0 == 2:
                self.led2.value(value0)
                pass
            elif num0 == 3:
                self.led3.value(value0)
                pass
            elif num0 == 4:
                self.led4.value(value0)
                pass
            elif num0 == 5:
                self.led5.value(value0)
                pass

            pass
        else :
            self.led1.value(value0)
            self.led2.value(value0)
            self.led3.value(value0)
            self.led4.value(value0)
            self.led5.value(value0)
            pass

        pass

    def print_debug(self, content=''):
        '''
        replace the original print function to another debug bus
        '''
        if self.sim_mcu == 1:
            # real mode change output to the debug bus
            self.uart1.write(content)
        else:
            print(content)
            pass

        pass

    def wait_cmd(self):
        '''
        command input structure
        '''

        cmd_in_raw = input()
        self.led_toggle()

        # split command with '.'
        self.cmd_array = cmd_in_raw.split('.')
        '''
        deifnition of command

        I2C.{device;XX}.{register;XX}.{data;XX}
        PWM.{frequency;Hz}.{duty;%}.{en;0 or 1}
        PIO.
        GPIO.{number}.{}


        '''

    def pico_emb_main(self):
        '''
        pico main program
        '''

        while 1 :

            self.wait_cmd()



        pass


pico_grace= pico_emb(sim_mcu0=sim_mode)
# pico_grace.pico_emb_main()
# pico_grace.debug_led(num0=1, value0=1, all=1)
