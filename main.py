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

        # ===== input command
        self.cmd_array = []

        self.sim_mcu = sim_mcu0

        # ===== the only LDE on PICO, reserve for LED
        self.led = machine.Pin(25, machine.Pin.OUT)

        # ===== UART- debug bus settings
        self.baud_r_com = 9600
        self.uart1 = machine.UART(1, baudrate=self.baud_r_com, tx=Pin(4), rx=Pin(5))  # 替换Pin(4)和Pin(5)为实际的引脚

        # ===== debug led settings (don't use after model test finished)
        self.led1 = machine.Pin(1, machine.Pin.OUT)
        self.led2 = machine.Pin(9, machine.Pin.OUT)
        self.led3 = machine.Pin(13, machine.Pin.OUT)
        self.led4 = machine.Pin(18, machine.Pin.OUT)
        self.led5 = machine.Pin(22, machine.Pin.OUT)

        # ===== general IO pin configuration
        # the name of self.io_x doesn't , name will change with array
        # and the mapping setting should be correct
        # only change the mapped definition and call the correct pin from host
        self.io_ind = [8, 9, 10, 11, 12, 13]
        self.io_8 = machine.Pin(self.io_ind[0], machine.Pin.OUT)
        self.io_9 = machine.Pin(self.io_ind[1], machine.Pin.OUT)
        self.io_10 = machine.Pin(self.io_ind[2], machine.Pin.OUT)
        self.io_11 = machine.Pin(self.io_ind[3], machine.Pin.OUT)
        self.io_12 = machine.Pin(self.io_ind[4], machine.Pin.OUT)
        self.io_13 = machine.Pin(self.io_ind[5], machine.Pin.OUT)
        # IO reference define: name(GPIO number):IO_object
        self.io_ref_array = { str(self.io_ind[0]):self.io_8, str(self.io_ind[1]):self.io_9, str(self.io_ind[2]):self.io_10,
                             str(self.io_ind[3]):self.io_11, str(self.io_ind[4]):self.io_12, str(self.io_ind[5]):self.io_13}
        # the value function without input will return the result
        # self.io_status_array = { '8':0, '9':0, '10':0, '11':0, '12':0, '13':0}
        # status of the IO can be read directly from the => pin_status = pin.value()

        # ===== PIO pin configuration
        self.en_ind = 6
        self.sw_ind = 7
        self.mode_index = 1
        self.en_pin = machine.Pin(self.en_ind, machine.Pin.OUT)
        self.sw_pin = machine.Pin(self.sw_ind, machine.Pin.OUT)

        # ===== PWM default configuration
        # manual will be PICO obj or PWM object in PICO side
        self.pwm0 = machine.PWM(Pin(0), freq=25000000, duty_u16=32765)
        self.pwm1 = machine.PWM(Pin(0), freq=25000000, duty_u16=32765)

        # ===== I2C Bus configuration

        # ===== relay control configuration
        # relay array, need to have sequence define in source code
        self.relay_ind = [16, 17, 18, 19, 20, 21, 22, 26, 27, 28]
        # status of the IO can be read directly from the => pin_status = pin.value()
        self.relay0 = machine.Pin(self.relay_ind[0], machine.Pin.OUT)
        self.relay1 = machine.Pin(self.relay_ind[1], machine.Pin.OUT)
        self.relay2 = machine.Pin(self.relay_ind[2], machine.Pin.OUT)
        self.relay3 = machine.Pin(self.relay_ind[3], machine.Pin.OUT)
        self.relay4 = machine.Pin(self.relay_ind[4], machine.Pin.OUT)
        self.relay5 = machine.Pin(self.relay_ind[5], machine.Pin.OUT)
        self.relay6 = machine.Pin(self.relay_ind[6], machine.Pin.OUT)
        self.relay7 = machine.Pin(self.relay_ind[7], machine.Pin.OUT)
        self.relay8 = machine.Pin(self.relay_ind[8], machine.Pin.OUT)
        self.relay9 = machine.Pin(self.relay_ind[9], machine.Pin.OUT)
        # IO reference define: name(GPIO number):IO_object
        self.relay_ref_array = { str(self.relay_ind[0]):self.relay0, str(self.relay_ind[1]):self.relay1, str(self.relay_ind[2]):self.relay2, str(self.relay_ind[3]):self.relay3,
                             str(self.relay_ind[4]):self.relay4, str(self.relay_ind[5]):self.relay5, str(self.relay_ind[6]):self.relay6, str(self.relay_ind[7]):self.relay7,
                             str(self.relay_ind[8]):self.relay8, str(self.relay_ind[9]):self.relay9}

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

        # split command with ';'
        self.cmd_array = cmd_in_raw.split(';')
        self.print_debug(f'split cmd is : {self.cmd_array}')
        self.print_debug(f'mode: {self.cmd_array[0]}')

        # print the command out
        for i in range (0, len(self.cmd_array), 1):
            print(f'item {i}, is {self.cmd_array[i]}')


        '''
        deifnition of command

        i2c;{device-XX};{register-XX};{read/write};{data-XX or length-x}
        pwm;{frequency-Hz};{duty-%};{en-0 or 1}
        pio;
        gio;{number};{status-1 or 0}
        p_mode;{1-4}
        # mode sequence: 1-4: (EN, SW) = (0, 0),  (0, 1), (1, 0), (1, 1) => default normal
        gio;8;1


        '''
        pass

    def i2c_read(self, device=0, regaddr=0, len=1):

        pass

    def i2c_write(self, device=0, regaddr=0, datas=0):

        pass

    def io_change(self, num0='', status0=0):
        '''
        change IO => refer to pin out definition
        update initialization based on the definition
        minimum toggle time without print, "within 100us"
        '''
        num0 = str(num0)
        if status0 == 1 or status0 == 0 :
            self.io_ref_array[num0].value(status0)
        # 231109 there are IO delay concern for minimum toggling time in this function
        # cancel the print function after debug finished
        # print time is based on the UART port operation and baud rate
        # self.print_debug(f'io_change, ch {num0}, status {status0}')
        # time.sleep_us(0)

        pass

    def io_reset(self, pio_reset=0):
        '''
        set all to 0
        just general IO, no PIO
        '''

        x_c = len(self.io_ref_array)
        x = 0
        while x < x_c :
            temp_io = list(self.io_ref_array.values())[0]
            temp_io.value(0)
            x = x + 1
            pass

        self.print_debug(f'io_reset done')

        if pio_reset == 1:
            # PIO also reset, reset to all 0
            self.pmic_mode(1)

        pass

    def pmic_mode(self, mode_index=4):
        '''
        (EN,SW) or (EN2, EN1) \n
        1:(0,0); 2:(0,1); 3:(1,0); 4:(1,1)
        GP6: EN (EN2)
        GP7: SW (EN1)
        '''
        # normal condition is IO, both IO and pulse IO are ok
        self.mode_index = mode_index
        if self.mode_index == 1:
            self.io_change(num0=str(self.en_ind), status0=0)
            self.io_change(num0=str(self.sw_ind), status0=0)
            pass
        elif self.mode_index == 2:
            self.io_change(num0=str(self.en_ind), status0=0)
            self.io_change(num0=str(self.sw_ind), status0=1)
            pass
        elif self.mode_index == 3:
            self.io_change(num0=str(self.en_ind), status0=1)
            self.io_change(num0=str(self.sw_ind), status0=0)
            pass
        elif self.mode_index == 4:
            self.io_change(num0=str(self.en_ind), status0=1)
            self.io_change(num0=str(self.sw_ind), status0=1)
            pass
        else:
            self.print_debug(f'command :{mode_index} is invalid, no action')
            pass

        pass

    def relay_ctrl(self, channel_index=0):
        '''
        self.relay_ref_array = [16, 17, 18, 19, 20, 21, 22, 26, 27, 28]
        from 0 to 9 \n
        MCU IO need to be match with array setting
        '''

        pass

    def ezcommand(self, command0):
        '''
        same operation with JIGM3, transfer code to string,
        need to prevent reserve words conflict
        '''

        pass



    def pico_emb_main(self):
        '''
        pico main program
        '''

        while 1 :

            self.wait_cmd()

            if self.cmd_array[0] == 'i2c' :
                # self.i2c_read

                pass
            elif self.cmd_array[0] == 'gio' :
                self.io_change(num0=self.cmd_array[1], status0=int(self.cmd_array[2]))
                pass
            elif self.cmd_array[0] == 'pio' :
                pass
            elif self.cmd_array[0] == 'pwm' :
                pass
            elif self.cmd_array[0] == 'en_mode' :
                pass
            elif self.cmd_array[0] == 'grace' :
                self.io_change(num0=self.cmd_array[1], status0=int(1))
                self.io_change(num0=self.cmd_array[1], status0=int(0))
                pass



        pass


pico_grace= pico_emb(sim_mcu0=sim_mode)
# pico_grace.pico_emb_main()
# pico_grace.debug_led(num0=1, value0=1, all=1)

pico_grace.pico_emb_main()
