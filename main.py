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

# ==== 240213: add the import of module
'''
this is the led module of YD-2040 using GPIO23 as LED control
GPIO23 will also be reserve in the original PICO for competible with add
hardware
'''
import pio_ws2812_obj as rgb_led


'''
difference between pico, pico W and YD-2040
YD-2040:
> need to connect R68 and Vref for the LED and ADC
> GPIO23 => LED, GPIO24 => user button
> Run => RST button
PICO:
> GPIO23 => PFM, PWM selection, GPIO24 => Input bus detection
PICO W:
'''




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

        # 将引脚设置为默认上拉 (only for YD2040)
        # self.button_in = Pin(24, Pin.IN, Pin.PULL_UP)

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

        # # add backup for the not using debug led
        # self.led1 = self.led
        # self.led2 = self.led
        # self.led3 = self.led
        # self.led4 = self.led
        # self.led5 = self.led

        # ===== PIO pin configuration
        # for the initialization of PIO in asm_pio => set_init=rp2.PIO.OUT_LOW
        # OUT_LOW or OUT_HIGH can be used for default state
        self.en_ind = 6
        self.sw_ind = 7
        self.mode_index = 1
        self.en_pin = machine.Pin(self.en_ind, machine.Pin.OUT)
        self.sw_pin = machine.Pin(self.sw_ind, machine.Pin.OUT)

        # ===== general IO pin configuration
        # the name of self.io_x doesn't , name will change with array
        # and the mapping setting should be correct
        # only change the mapped definition and call the correct pin from host
        self.io_ind = [8, 9, 10, 11, 12, 13]
        self.io_0 = machine.Pin(self.io_ind[0], machine.Pin.OUT)
        self.io_1 = machine.Pin(self.io_ind[1], machine.Pin.OUT)
        self.io_2 = machine.Pin(self.io_ind[2], machine.Pin.OUT)
        self.io_3 = machine.Pin(self.io_ind[3], machine.Pin.OUT)
        self.io_4 = machine.Pin(self.io_ind[4], machine.Pin.OUT)
        self.io_5 = machine.Pin(self.io_ind[5], machine.Pin.OUT)
        # IO reference define: name(GPIO number):IO_object
        # self.io_ref_array = {str(self.io_ind[0]):self.io_0, str(self.io_ind[1]):self.io_1, str(self.io_ind[2]):self.io_2,
        #                      str(self.io_ind[3]):self.io_3, str(self.io_ind[4]):self.io_4, str(self.io_ind[5]):self.io_5}
        # 240102 cancel the old reference array, change to new below
        self.io_ref_array = [self.io_0, self.io_1, self.io_2, self.io_3, self.io_4, self.io_5, self.en_pin, self.sw_pin]

        # the value function without input will return the result
        # self.io_status_array = { '8':0, '9':0, '10':0, '11':0, '12':0, '13':0}
        # status of the IO can be read directly from the => pin_status = pin.value()



        # ===== PWM default configuration
        # manual will be PICO obj or PWM object in PICO side
        self.freq_set = 1000000
        self.pwm_scaling = 1000
        self.pwm0_pin = 2
        self.pwm1_pin = 3
        # duty 0 is default low
        self.pwm0 = machine.PWM(Pin(self.pwm0_pin), freq=self.freq_set, duty_u16=0)
        self.pwm1 = machine.PWM(Pin(self.pwm1_pin), freq=self.freq_set, duty_u16=0)

        # ===== I2C Bus configuration
        self.i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

        # 230920 add I2C bit write function
        # 231117: this can be put at the PICO_obj (python side, not micropython side)

        # ===== relay control configuration
        # relay array, need to have sequence define in source code
        self.relay_ind = [14, 15, 20, 21, 22, 26, 27, 28, 4, 5]
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
        # self.relay_ref_array = { str(self.relay_ind[0]):self.relay0, str(self.relay_ind[1]):self.relay1, str(self.relay_ind[2]):self.relay2, str(self.relay_ind[3]):self.relay3,
        #                      str(self.relay_ind[4]):self.relay4, str(self.relay_ind[5]):self.relay5, str(self.relay_ind[6]):self.relay6, str(self.relay_ind[7]):self.relay7,
        #                      str(self.relay_ind[8]):self.relay8, str(self.relay_ind[9]):self.relay9}
        # 240102 cancel the old reference array, change to new below
        self.relay_ref_array = [self.relay0, self.relay1, self.relay2, self.relay3, self.relay4, self.relay5, self.relay6, self.relay7, self.relay8, self.relay9]


        # default set to 100, not active reset process at the first time
        self.active_relay_ch = 100

        # ===== engineering mode assignment and initialization

        # 231116 to map with JIGM3, need to use s
        # only micropython have sleep_us, ms, not use in general input
        # only for micropython operation
        self.relay_dly = 0.02

        # reset all the LED
        self.debug_led(num0=1, value0=0, all=1)

        self.io_reset(ind_type0='relay')
        # 240117 change the setting of PIO_reset to 0, keep the same
        # default setting for the MCU
        self.io_reset(ind_type0='io', pio_reset=0)
        self.pmic_mode()
        self.w_led = rgb_led.ws2812_LED()
        # bring the default LED to make sure LED_obj works fine
        self.w_led.set_LED()

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

    def print_debug(self, content='', always_print0=0):
        '''
        replace the original print function to another debug bus

        '''
        if self.sim_mcu == 1 and always_print0 == 1 :
            # real mode change output to the debug bus
            # 240117 change to print all in UART and sim_mcu = 2 allow print to USB COM
            # self.uart1.write(content)
            pass
        elif self.sim_mcu == 2:
            # pico connect and need to check termainal
            self.uart1.write(content)
            if always_print0 == 1 :
                print(content)
        elif self.sim_mcu == 0:
            print(content)
            pass

        pass

    def wait_cmd(self):
        '''
        command input structure
        '''
        self.print_debug(content=f'Dear Grace, pico is ready for you :)', always_print0=1)
        # command update everytime here, no need to worry for infinite loop
        cmd_in_raw = input()
        self.print_debug(f'input cmd is :{cmd_in_raw}')
        self.led_toggle()

        # split command with ';'
        self.cmd_array = cmd_in_raw.split(';')
        self.print_debug(f'split cmd is : {self.cmd_array}')
        self.print_debug(f'mode: {self.cmd_array[0]}')

        # print the command out
        for i in range (0, len(self.cmd_array), 1):
            self.print_debug(f'item {i}, is {self.cmd_array[i]}')


        '''
        deifnition of command

        fromat:
        i2c;{device-XX};{register-XX};{r_read/w_write};{length-x or data-[1,2,3,4,5]}
        pwm;{frequency-kHz};{duty-%};{type-0(duty) or 1(ns)};{channel 0(PWM0) or 1(PWM1)}
        pio;{number- 6(EN), 7(SW)};{pulse_count(<255)}
        gio;{number- 0 to 9};{status- 0_off, 1_on}
        en_mode;{(EN,SW) or (EN2, EN1) => 1:(0,0); 2:(0,1); 3:(1,0); 4:(1,1)}
        rly;{channel_active- 0 to 9}

        '''
        pass

    def i2c_read(self, device=0, regaddr=0, len=1):
        '''
        read different length
        '''
        # 发送要读取的寄存器地址

        self.i2c.writeto(device, bytes([regaddr]))
        self.print_debug(content=f'reg_addr= {regaddr}, and byte {bytes([regaddr])}', always_print0=1)
        # 从I2C设备读取数据
        data_bytes = self.i2c.readfrom(device, len)  # 4表示要读取的字节数

        # numeric_list = [byte for byte in data_bytes]
        # hex_array = [hex(x)[2:] for x in numeric_list]

        # 240123 new method, refer to the modification of i2c read example
        # 將每個字節轉換為十六進制字符串，並使用逗號分隔
        hex_strings = ", ".join([hex(byte) for byte in data_bytes])
        # 去除 "0x" 並分割字符串
        hex_values = hex_strings.replace("0x", "").split(", ")
        # 將每個字符串轉換為十進制整數，再轉換為固定兩位的十六進制字符串
        byte_list = ["{:02X}".format(int(value, 16)) for value in hex_values]

        self.print_debug(content=f'data read= {data_bytes}, hex is: {hex_strings} and output {byte_list}', always_print0=1)

        # print to pico termainal, being read from PC
        # print(numeric_list)
        # return numeric_list
        print(byte_list)
        return byte_list


    def i2c_write(self, device=0, regaddr=0, datas=0):
        '''
        write different length
        data can be array input, using the array of number within 0-255 (FF), will
        be data input to the slave started from the setting regaddr
        '''

        '''
        different between writeto and writeto_mem:
        i2c.writeto(address, data, stop=True)
        i2c.writeto_mem(address, register, data, stop=True)
        note: 'stop' is to choose sending the stop or not after finished, default True
        '''

        self.print_debug(content=f'regaddr = {regaddr}, no need to change', always_print0=1)
        n_datas = bytes([datas])
        self.print_debug(content=f'data_in = {datas}, hex: {hex(datas)} and SDA_out {n_datas}', always_print0=1)
        self.i2c.writeto_mem(device, regaddr, n_datas)
        print(f'write_love_to_grace_XD')

        pass

    def io_change(self, num0='', status0=0):
        '''
        change IO => refer to pin out definition
        update initialization based on the definition
        minimum toggle time without print, "within 100us"
        '''
        num0 = int(num0)
        # num0 = str(num0)
        if self.sim_mcu >= 1:
            if status0 == 1 or status0 == 0 :
                self.io_ref_array[num0].value(status0)
                # self.io_ref_array[num0].value(status0)
                # 240102: don't use the sequence of discionary in micropython
                # it's not follow the definition (before python 3.7 don't have
                # sequence)
                # list(self.io_ref_array.values())[num0].value(status0)
                # print(list(self.io_ref_array.values())[num0])
                # print(self.io_ind)
                # print(self.io_8)
                # print(self.io_9)
                # print(self.io_10)
                # print(self.io_11)
                # print(self.io_12)
                # print(self.io_13)
                # print(self.io_ref_array)
                # print(self.relay_ref_array)
                pass
            # 231109 there are IO delay concern for minimum toggling time in this function
            # cancel the print function after debug finished
            # print time is based on the UART port operation and baud rate
            # self.print_debug(f'io_change, ch {num0}, status {status0}')
            # time.sleep_us(0)
            # self.print_debug(f'grace_trigger_IO:{num0} to status {status0}_QQ, mapped io on pico is {self.io_ref_array[num0]}')
            pass

        else:
            self.print_debug(content=f'io change in sim mode, with num0:{num0}, state:{status0}')

        pass

    def io_reset(self, ind_type0='relay', pio_reset=0):
        '''
        set all to 0
        just general IO, no PIO, PIO default is high (EN, SW)
        '''
        if ind_type0 == 'relay':
            # reset the relay related io pin
            ind_arry0 = self.relay_ref_array
        else:
            # send the io index array for reset
            ind_arry0 = self.io_ref_array

        x_c = len(ind_arry0)
        x = 0
        while x < x_c :
            temp_io = ind_arry0[x]
            temp_io.value(0)
            x = x + 1
            pass

        self.print_debug(f'io_reset for {ind_type0} done',always_print0=1)

        if pio_reset == 1:
            # PIO also reset, reset to all 0
            self.pmic_mode(1)

        pass

    def relay_rst(self, type0='relay'):
        '''
        reset all relay => 231128, no need to reset all,
        just turn off the previous on channel
        to reset all io by this function, enter: 'io'
        '''

        io_arry = self.relay_ref_array
        if type0 == 'io':
            io_arry = self.io_ref_array

        for io_ch in io_arry:
            io_ch.value(0)
            self.print_debug(f'channel {io_ch} reset done')
            pass

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
            self.en_pin.value(0)
            self.sw_pin.value(0)
            pass
        elif self.mode_index == 2:
            self.en_pin.value(0)
            self.sw_pin.value(1)
            pass
        elif self.mode_index == 3:
            self.en_pin.value(1)
            self.sw_pin.value(0)
            pass
        elif self.mode_index == 4:
            self.en_pin.value(1)
            self.sw_pin.value(1)
            pass
        else:
            self.print_debug(f'command :{mode_index} is invalid, no action', always_print0=1)
            pass

        pass

    def relay_ctrl(self, channel_index=0, t_dly_s=0.0):
        '''
        self.relay_ind = [16, 17, 18, 19, 20, 21, 22, 26, 27, 28]
        from 0 to 9 \n
        MCU IO need to be match with array setting
        '''
        '''
        relay control method: need to add programmable delay between switching
        default 20, change by grace(engineering mode)
        '''
        if t_dly_s != 0:
            # change settings if there are input
            self.relay_dly = t_dly_s


        # reset active relay channel, skip if ch_ind is 100
        if self.active_relay_ch != 100:
            # reset the relay channel
            self.relay_ref_array[int(self.active_relay_ch)].value(0)

        time.sleep(self.relay_dly)

        # update turn off index
        self.active_relay_ch = channel_index
        # open new relaly channel
        self.relay_ref_array[int(self.active_relay_ch)].value(1)

        pass


    """
    # 231117: remember that some code can be put at the python side
    # JtIGM3 is the python side of MCU interface, we are only targe
    # GPLV4 not to cover all function in JIGM3 => it shuld be PICO_obj

    def bit_s(self, bit_num0=0, byte_state_tmp0=0):
        bit_num0 = str(bit_num0)

        # bit set process
        bit_cmd0 = self.bit_set[bit_num0]
        self.print_debug(f"set bit_cmd0 is {bit_cmd0}")
        new_byte_data = byte_state_tmp0 | bit_cmd0
        self.print_debug(f"final command0 is {new_byte_data}, g")

        return new_byte_data

    def bit_c(self, bit_num0=0, byte_state_tmp0=0):
        bit_num0 = str(bit_num0)

        # bit clear process
        bit_cmd0 = self.bit_clr[bit_num0]
        self.print_debug(f"clear bit_cmd0 is {bit_cmd0}")
        new_byte_data = byte_state_tmp0 & bit_cmd0
        self.print_debug(f"final command0 is {new_byte_data}, g")

        return new_byte_data

    def hex_to_num(self, data_in0=''):
        '''
        try to transfer the input to number for register write
        skip if already number (but watch out this is dec number input, not hex)
        '''
        try:
            data_in0 = int(data_in0, 16)
            self.print_debug(f'input is string and transfer number: {data_in0}')
        except:
            self.print_debug(f'input is already number: {data_in0}, return origin')

        return data_in0

    def num_to_hex (self, data_in0=0):
        '''
        transfer the number to hex
        '''
        try:
            data_in0 = hex(data_in0)
            return data_in0
        except:
            self.print_debug(f'input data "{data_in0}" transfer error, double check input data')
            return 'data_error'

        pass

    """

    def pio_pulse_gen(self, pulse_gear_us=0.1, default_state='LOW'):

        pass

    def io_pulse_gen(self, pulse_amount0=1, pulse_type0='LOW', duration_set=0, num0=0):
        '''
        num0 = io_ind or pio(en_ind, sw_ind), both are ok
        by using loop to IO command generate the pulse output
        the minimum duration is 100us (1 counter 100us)
        => 231113 change to use different functino for gio and pio
        240205: duration_set = 0 => 10us pulse

        '''

        # io pin selection
        self.io_temp = self.io_ref_array[int(num0)]
        # error command check index
        self.io_state_lock = 0
        # io_transition state
        self.io_tran = 0
        '''
        this is 100us constant calibration index
        adjust for pulse width
        set 0 is 10us
        set 85 is 100us
        delay command cause 5us @ 250MHz
        '''

        self.us_counter_cal = 0
        if duration_set != 0 :
            # change the duration to 100us
            self.us_counter_cal = 85

        if self.sim_mcu == 1 :
            self.io_state0 = self.io_temp.value()
        else :
            # sim mode example is low pulse
            self.io_state0 = 1

        # io_state should be:
        if pulse_type0 == 'LOW':
            self.io_state_lock = 1
            self.io_tran = 0
        elif pulse_type0 == 'HIGH':
            self.io_state_lock = 0
            self.io_tran = 1

        if self.io_state0 == self.io_state_lock :
            # valid pulse request
            # string command used as follow

            self.str_cmd = '''self.io_temp.value(self.io_state_lock)\n'''

            '''
            # string caculated example :
            # == default
            self.io_temp.value(self.io_state_lock)

            # == pulse element
            time.sleep_us(self.us_counter_cal)
            self.io_temp.value(self.io_tran)
            time.sleep_us(self.us_counter_cal)
            self.io_temp.value(self.io_state_lock)
            '''

            single_pulse = '''time.sleep_us(self.us_counter_cal)
self.io_temp.value(self.io_tran)
time.sleep_us(self.us_counter_cal)
self.io_temp.value(self.io_state_lock)
'''
            self.print_debug(f'the single pulse command is {single_pulse}')
            x_pulse = 0
            while x_pulse < int(pulse_amount0) :

                self.str_cmd = self.str_cmd + single_pulse
                # maybe it's able to compare with using loop with direct command change
                # optional performance comparison
                self.print_debug(content=f'pulse_count x in {x_pulse} {pulse_amount0}')
                self.print_debug(content=f'command become \n{self.str_cmd}')

                x_pulse = x_pulse + 1
                pass
            self.print_debug(f'the final command is \n{self.str_cmd}')

        else:
            # invalid pulse request
            self.print_debug(f'invalid pulse request for pin: {num0}, default state: {self.io_state0} with {pulse_type0} pulse request', always_print0=1)

        if self.sim_mcu >= 1:
            # this is micropython command which causing crash during sim mode
            # exec(self.str_cmd)
            self.str_to_code(string0=self.str_cmd)

        self.print_debug(f'pulse finished with: \n{self.str_cmd} \n, hey cute Grace, is this correct?~ ? ',always_print0=1)

        pass

    def pwm_ctrl(self, freq0=None, duty0=0.0, type0=0, ch0=0):
        """
        duty is either % or duration_ns, depends on type
        type: 0- duty in %, 1- duration_ns
        if no freq setting, freq set to default
        set duty to 0 to disable
        1000 is default freq scaling, freq_final = scaling*freq0, default 1MHz
        """

        if freq0 == None:
            # use default setting for frequency
            freq0 = self.freq_set
        else:
            freq0 = int(float(freq0)*self.pwm_scaling)

        if type0 == 0:
            # duty in %
            duty_nor = float(duty0) / 100
            duty_res = int(duty_nor * 65535)
            pass
        else:
            # duty in ns, no need for process
            duty_res = int(duty0)
            pass

        if ch0 == 0:
            # active pwm0
            if type0 == 0:
                # % mode
                pwm0 = machine.PWM(Pin(self.pwm0_pin), freq=freq0, duty_u16=duty_res)
            else:
                # ns mode
                pwm0 = machine.PWM(Pin(self.pwm0_pin), freq=freq0, duty_ns=duty_res)
        elif ch0 == 1:
            # active pwm0
            if type0 == 0:
                # % mode
                pwm1 = machine.PWM(Pin(self.pwm1_pin), freq=freq0, duty_u16=duty_res)
            else:
                # ns mode
                pwm1 = machine.PWM(Pin(self.pwm1_pin), freq=freq0, duty_ns=duty_res)

        pass

    def sim_assign(self, *args, **kwargs):
        '''
        the simulation mode input with different amount of variable input
        => virtual machine for PICO
        *args is variable input; **kwargs is dictionary input
        refer to python, parameter loaded for further information,
        there are example setting the test mode to 1.5
        to access input variable:
        print('this is kwargs 1 ' + str(kwargs['para1']))
        print('this is args 1 ' + str(args[0]))
        '''
        # save the input to list and kwargs
        self.sim_args = args
        self.sim_kwargs = kwargs
        pass

    def dedent_skip_1(self, code):
        lines = code.split('\n')
        # 计算最小缩进
        min_indent = float('inf')
        for line in lines[1:]:  # 跳过第一行，因为它通常是模块级别的缩进
            stripped = line.lstrip()
            if stripped:
                indent = len(line) - len(stripped)
                min_indent = min(min_indent, indent)

        # 移除最小缩进
        dedented_lines = [line[min_indent:] for line in lines]
        dedented_code = '\n'.join(dedented_lines)
        return dedented_code

    def dedent(self, code):
        lines = code.split('\n')
        # 计算最小缩进
        min_indent = float('inf')
        for line in lines:
            stripped = line.lstrip()
            if stripped:
                indent = len(line) - len(stripped)
                min_indent = min(min_indent, indent)

        # 移除最小缩进
        dedented_lines = [line[min_indent:] for line in lines]
        dedented_code = '\n'.join(dedented_lines)
        return dedented_code

    def execute_indented_code(self, code):
        '''
        check previous format as adjustment reference
        input the code in string and return the modify result
        '''
        # 获取执行上下文的缩进
        current_indent = ' ' * (len(code) - len(code.lstrip()))

        # 在代码块的每一行前添加当前缩进
        indented_code = '\n'.join([current_indent + line for line in code.split('\n')])

        # not to exute here, operate all the excution in 'str_to_code'
        # # 执行代码块
        # exec(indented_code)

    def str_to_code(self, string0="", *args, **kwargs ):
        '''
        function run for string command, also include the adjustment of 'TAB'
        to prevent error for the operation
        '''
        # # 231114, this is just testing string for the debugging
        # string0 = '''self.print_debug(content=f'Grace went back home now', always_print0=1)'''

        # 231114: add the reference dictionary to the exec function
        self.str_code_ref = {'self': self}
        # merge the self object with kwargs for cute Grace
        self.str_code_ref.update(kwargs)

        try:
            # string0 = str(string0)
            # textwrap => can't be used, give up and just for record
            # string0 = textwrap.dedent(string0)

            # there seems to have error
            string0 = self.dedent(string0)
            # 240131 if need the return result of string, use "eval" to replace "exec"
            exec(string0, globals(), self.str_code_ref)

            # self.execute_indented_code(string0)
        except Exception as e:
            self.print_debug(f'exception: {e}', always_print0=1)
            # 231114: watchout! don't use try-except too early
            # or you may not see the issue
            self.print_debug(content=f'there are some issue of exec() \n with string \n{string0}', always_print0=1)
        pass

    def universal_command(self, cmd0):
        '''
        accept different command during operation for flexible adjustment of
        program flow, or used to add new interrupt during operation
        240123: plan to add the function of 1-add cmd, 2-print cmd, 3-excution
        '''
        self.str_to_code(cmd0)

        pass

    # # 231117 this function have operation limitation, move to pico_obj at python side
    # # PICO @ micropython can only have i2c read and write, receive the finished command
    # # python side program capability is better, no need to be put at micropython
    # def pure_group_write(self, lsb0=0, len0=1, data0=0, byte_state_tmp0=0):
    #     pass

    def pico_emb_main(self):
        '''
        pico main program
        > extra return information will be added at main, not in single
        function (general print items)
        > for special return (i2c read...) will be print(return) in single function
        '''

        pwr_signal = 0
        while 1 :

            if pwr_signal == 0 :
                # power up before wait command, toggle LED for PWR up
                self.w_led.set_LED(red=1,green=0,blue=0)
                self.led_toggle(duration=0.3)
                self.w_led.set_LED(red=0,green=1,blue=0)
                self.led_toggle(duration=0.3)
                self.w_led.set_LED(red=0,green=0,blue=1)
                self.led_toggle(duration=0.3)
                self.w_led.set_LED(red=0,green=1,blue=0)
                pwr_signal = 1

            self.wait_cmd()

            # only one try - except is needed for checking
            try:

                if self.cmd_array[0] == 'i2c' :
                    # transfer address and data to get ready
                    device0 = int(self.cmd_array[1])
                    reg_addr0 = int(self.cmd_array[2])
                    if self.cmd_array[3] == 'w' :
                        # i2c write
                        integer_string = self.cmd_array[-1]
                        # 使用負數索引時，-1 表示列表的最後一個元素，-2 表示倒數第二個元素，以此類推。這是 Python 中常見的索引運算方式。
                        # 使用 eval 函數將字符串轉換為列表
                        data_list = eval(integer_string)
                        # 231128 data no need to split, pass the array directly
                        # transfer to byte inside the write function, only pass the datas into
                        self.i2c_write(device=device0,regaddr=reg_addr0,datas=data_list)
                        # return is in function
                        pass
                    elif self.cmd_array[3] == 'r' :
                        # i2c read
                        # 240117 for the read, need to check the format of the output
                        self.i2c_read(device=device0,regaddr=reg_addr0,len=int(self.cmd_array[4]))
                        # return is in function
                        pass
                    pass
                elif self.cmd_array[0] == 'gio' :
                    self.io_change(num0=self.cmd_array[1], status0=int(self.cmd_array[2]))
                    # return item below
                    print(f'g_gio_{self.cmd_array[1]}_pin_{self.io_ref_array[int(self.cmd_array[1])]}_status_{self.cmd_array[2]}')
                    pass
                elif self.cmd_array[0] == 'pio' :
                    '''
                    240205 first version of PIO is just low pulse output (glitch can only be done
                    by the JIGM3 tool, since the pattern is't ready yet)
                    '''

                    self.io_pulse_gen(pulse_amount0=int(self.cmd_array[2]), pulse_type0='LOW', duration_set=0, num0=int(self.cmd_array[1]))
                    # return item below
                    print(f'Grace_say_other_comming_soon, now only 10us low pulse')
                    pass
                elif self.cmd_array[0] == 'pwm' :
                    self.pwm_ctrl(freq0=float(self.cmd_array[1]),duty0=float(self.cmd_array[2]),type0=int(self.cmd_array[3]),ch0=int(self.cmd_array[4]))
                    # return item below
                    print(f'g_pwm_f_{self.cmd_array[1]}_D_{self.cmd_array[2]}_t_{self.cmd_array[3]}_ch_{self.cmd_array[4]}')
                    pass
                elif self.cmd_array[0] == 'en_mode' :
                    self.pmic_mode(int(self.cmd_array[1]))
                    # return item below
                    print(f'Grace_mode_{self.cmd_array[1]}')
                    pass
                elif self.cmd_array[0] == 'rly' :
                    r_ch = int(self.cmd_array[1])
                    self.relay_ctrl(r_ch)
                    print(f'Grace_relay_{self.cmd_array[1]}_pin_{self.relay_ind[r_ch]}')
                    pass
                elif self.cmd_array[0] == 'grace' :
                    # engineering mode, parameter change or special function

                    # for invalid data input or every error, all assign to fail
                    if self.cmd_array[1] == 'relay_dly' :
                        # change relay delay time
                        self.relay_dly = int(self.cmd_array[2])
                        print(f'relay_dly_def_change_{self.relay_dly}')
                        pass
                    if self.cmd_array[1] == 'pwm_scale' :
                        # change pwm scaling factor
                        self.pwm_scaling = int(self.cmd_array[2])
                        print(f'pwm_scaling_def_change_{self.pwm_scaling}')
                        pass
                    if self.cmd_array[1] == 'io_rst' :
                        # reset io and relay
                        self.relay_rst()
                        self.relay_rst('io')
                        print(f'io_relay_reset')
                    pass

                elif self.cmd_array[0] == '*IDN?' :
                    # identify for the device to control
                    print(f'Grace')

                elif self.cmd_array[0] == 't' :
                    # testing pattern during development status
                    # try:
                    if self.cmd_array[1] == 'io' :
                        # io toggling test
                        # 231110 done
                        self.io_change(num0=self.cmd_array[2], status0=int(1))
                        self.io_change(num0=self.cmd_array[2], status0=int(0))
                        pass
                    if self.cmd_array[1] == 'p' :
                        # pattern gen testing
                        # 231115 wait for scope check for calibration
                        self.io_change(num0='0',status0=1)
                        self.print_debug('enter pattern gen test')
                        self.io_pulse_gen(pulse_amount0=10, pulse_type0='LOW', duration_set=1, num0=0)
                        pass
                    if self.cmd_array[1] == 'i' :
                        # i2c mode
                        # 231115 wait for real test
                        self.i2c_write(device=0x4E, regaddr=0xA3, datas=183)
                        x = self.i2c_read(device=0x4E, regaddr=0xA0, len=10)
                        self.print_debug(str(x))
                        pass
                    if self.cmd_array[1] == 'pw' :
                        # pwm mode (100kHz for base)
                        # 231116 testing pass
                        self.pwm_ctrl( freq0=int(int(self.cmd_array[2])),
                            duty0=int(self.cmd_array[3]), type0=int(self.cmd_array[4]), ch0=int(self.cmd_array[5]) )
                        pass
                    if self.cmd_array[1] == 'r' :
                        print(f'relay active')
                        self.relay_ctrl(channel_index=0,t_dly_s=0)
                        time.sleep_us(200)
                        self.relay_ctrl(channel_index=1,t_dly_s=0.05)
                        time.sleep_us(200)
                        self.relay_ctrl(channel_index=2,t_dly_s=0.1)
                        time.sleep_us(200)
                        self.relay_ctrl(channel_index=3,t_dly_s=0)
                        self.relay_rst(type0='relay')

                    if self.cmd_array[1] == 'usb' :
                        '''
                        usb_port command send testing
                        toggle LED for the pin 22 debug port
                        '''
                        c_tog = 5
                        x_tog = 0
                        self.debug_led(num0=2,value0=1)
                        while x_tog < c_tog:

                            self.debug_led(num0=int(5),value0=1)
                            time.sleep_ms(100)
                            self.debug_led(num0=int(5),value0=0)
                            time.sleep_ms(100)
                            x_tog = x_tog + 1
                            self.print_debug(f'now is at tog ={x_tog}')
                            pass
                        self.debug_led(num0=2,value0=0)
                        pass
                    # end of testing pattern
                    pass
                elif self.cmd_array[0] == 'u' :
                    # universal command, but need to reference to the function or source code
                    # this is single line universal command

                    self.str_to_code(string0=str(self.cmd_array[1]))
                    pass

                # end of try for Grace
                pass
            except Exception as e:
                self.print_debug(f'exception: {e}',always_print0=1)
                self.print_debug(f'command for engineering mode fail {self.cmd_array}',always_print0=1)
                pass

            # end pico main while

            pass


pico_grace= pico_emb(sim_mcu0=sim_mode)
# pico_grace.pico_emb_main()
# pico_grace.debug_led(num0=1, value0=1, all=1)
testmode = 0


if testmode == 1:
    # relay toggle testing
    while 1 :
        test_x = 0
        for test_a in range (0, 8):
            pico_grace.relay_ctrl(test_a)
            time.sleep_ms(400)
            # x=input()

        time.sleep_ms(1000)
elif testmode == 2:
    # IO testing
    while 1 :
        test_x = 0
        for test_a in range (0, 8):
            pico_grace.io_change(num0=f'{int(test_a)}', status0=1)
            time.sleep_ms(400)
            pico_grace.io_change(num0=f'{int(test_a)}', status0=0)
            time.sleep_ms(400)
            x=input()
        time.sleep_ms(1000)




pico_grace.pico_emb_main()
