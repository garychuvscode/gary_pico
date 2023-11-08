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
sim_mode = 0

class pico_emb():

    def __init__(self, sim_mcu0=0):

        # input command
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


        self.io_8 = machine.Pin(8, machine.Pin.OUT)
        self.io_9 = machine.Pin(9, machine.Pin.OUT)
        self.io_10 = machine.Pin(10, machine.Pin.OUT)
        self.io_11 = machine.Pin(11, machine.Pin.OUT)
        self.io_12 = machine.Pin(12, machine.Pin.OUT)
        self.io_13 = machine.Pin(13, machine.Pin.OUT)


        # IO reference define: name(GPIO number):IO_object
        self.io_ref_array = { '8':self.io_8, '9':self.io_9, '10':self.io_10, '11':self.io_11, '12':self.io_12, '13':self.io_13}
        # status of the IO can be read directly from the => pin_status = pin.value()
        # the value function without input will return the result
        # self.io_status_array = { '8':0, '9':0, '10':0, '11':0, '12':0, '13':0}

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
        self.print_debug(f'input cmd is :{cmd_in_raw}')
        self.led_toggle()

        # split command with '.'
        self.cmd_array = cmd_in_raw.split('.')
        self.print_debug(f'split cmd is :{self.cmd_array}')
        self.print_debug(f'mode: {self.cmd_array[0]}')
        for i in range ()
        '''
        deifnition of command

        I2C.{device;XX}.{register;XX}.{read/write}.{data;XX or length;x}
        PWM.{frequency;Hz}.{duty;%}.{en;0 or 1}
        PIO.
        GPIO.{number}.{status;1 or 0}
        GPIO.8.1


        '''
        pass

    def i2c_read(self, device=0, regaddr=0, len=1):

        pass

    def i2c_write(self, device=0, regaddr=0, datas=0):

        pass

    def io_change(self, num0=0, status0=0):
        '''
        change IO => refer to pin out definition
        update initialization based on the definition
        '''
        num0 = str(num0)
        if status0 == 1 or status0 == 0 :
            self.io_ref_array[num0].value(status0)
        self.print_debug(f'io_change, ch{num0}, status{status0}')

        pass

    def io_reset(self):
        '''
        set all to 0
        '''

        x_c = len(self.io_ref_array)
        x = 0
        while x < x_c :
            temp_io = list(self.io_ref_array.values())[0]
            temp_io.value(0)
            x = x + 1
            pass

        self.print_debug(f'io_reset done')
        pass

    def pico_emb_main(self):
        '''
        pico main program
        '''

        while 1 :

            self.wait_cmd()

            if self.cmd_array[0] == 'I2C' :
                # self.i2c_read

                pass



        pass


pico_grace= pico_emb(sim_mcu0=sim_mode)
# pico_grace.pico_emb_main()
# pico_grace.debug_led(num0=1, value0=1, all=1)

pico_grace.pico_emb_main()
