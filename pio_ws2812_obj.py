import array
import time
from machine import Pin
import rp2
import machine
     

class ws2812_LED (): 

    def __init__(self, gpio0=23, pio_block0=0, num_LED0=1, sim_mode0=1):

        # general initial items 

        self.sim_mode = sim_mode0
        self.baud_r_com = 9600
        self.uart1 = machine.UART(1, baudrate=self.baud_r_com, tx=Pin(4), rx=Pin(5))  # 替换Pin(4)和Pin(5)为实际的引脚
        

        self.module_name = 'ws2812_LED'
        # 設置要控制的 WS2812 LED 的數量
        self.NUM_LEDS = num_LED0

        # 定義 PIO 程序 ws2812
        @rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
        def ws2812():
            T1 = 2
            T2 = 5
            T3 = 3
            wrap_target()
            label("bitloop")
            out(x, 1)               .side(0)    [T3 - 1]
            jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
            jmp("bitloop")          .side(1)    [T2 - 1]
            label("do_zero")
            nop()                   .side(0)    [T2 - 1]
            wrap()

        # 創建 StateMachine 對象，將 ws2812 程序傳遞給它，並配置 PIO 的一些參數
        self.sm = rp2.StateMachine(int(pio_block0), ws2812, freq=8_000_000, sideset_base=Pin(int(gpio0)))

        # 啟動 StateMachine，準備接收 FIFO 中的數據
        self.sm.active(1)

        # 創建 array 來存儲 LED 的顏色數據 ('I' is )第一個參數 "I" 指定了數組中元素的類型，
        # 這裡的 "I" 表示每個元素都是一個無符號整數（即正整數），第二個參數 [0] 是一個列表，
        # 包含了初始值為 0 的一個元素，所以這個數組就只包含一個整數 0。
        self.ar = array.array("I", [0])


        # end of initialization
        pass 

    def reset_led_array(self): 
        '''
        reset the LED array
        '''
        self.ar = array.array("I", [0])

    def set_LED(self, red=0, green=5, blue=0, led_index=0): 
        '''
        update the input setting for the LED 
        short the R68 for YD2040
        led_index => default is 1 LED, index 0 
        '''
        self.reset_led_array()

        if red < 255 or green < 255 or blue < 255 : 
                
            # 將紅、綠、藍值組合成一個顏色數據，按照 WS2812 的順序排列
            color = (green << 16) | (red << 8) | blue
            
            # 將顏色數據放入 array 中
            # 240213: the case of more than 1 LED, need to double check in experiment
            self.ar[led_index] = color
            # print(self.ar)

            # 將 array 放入 StateMachine 的 FIFO 中，從而將顏色數據發送到 WS2812 LED
            self.sm.put(self.ar, 8)

            # 等待一段時間，以便觀察 LED 的顏色
            # time.sleep_ms(50)
            pass 

        pass 


    def set_LED0(self, limit0=255): 

        '''
        LED breath with the limitation input
        default sim_mode set to 1 => the real mode 
        '''

        # reset the array every time call for set LED 
        self.reset_led_array()

        # 主循環，設置 LED 的顏色
        while True:

            try: 
                # 對於每一顆 LED
                for led_index in range(self.NUM_LEDS):
                    # 根據給定的紅、綠和藍值，計算出顏色數據
                    break0 = 0 
                    red = int(input(f"Enter red value for LED {led_index + 1} (0-255): "))
                    green = int(input(f"Enter green value for LED {led_index + 1} (0-255): "))
                    blue = int(input(f"Enter blue value for LED {led_index + 1} (0-255): "))

                    if red > limit0 or green > limit0 or blue > limit0 : 
                        break0 = 1 
                        # set the break command and break the for loop with update
                        # this also include the overflow, it will become 0 
                        break

                
                    # 將紅、綠、藍值組合成一個顏色數據，按照 WS2812 的順序排列
                    color = (green << 16) | (red << 8) | blue
                    
                    # 將顏色數據放入 array 中
                    self.ar[led_index] = color
                    # print(self.ar)
                
                # 將 array 放入 StateMachine 的 FIFO 中，從而將顏色數據發送到 WS2812 LED
                self.sm.put(self.ar, 8)
                
                # 等待一段時間，以便觀察 LED 的顏色
                # time.sleep_ms(50)

                pass 

            except Exception as e:

                self.print_debug(f'now is error for LED: "{e}" and break',always_print0=1)

                # break the while loop and back to main 
                break

            if break0 == 1 : 
                #  enter too large value than limit, break the loop 
                self.print_debug(f'the input "{red}, {green}, {blue}" is too large, break the loop', always_print0=1)
                pass 

            # end of while loop 
            pass 

        # end of function
        pass 


    def breath_type(self, c_count0=5, max0=20): 
        f'''
        auto run {c_count0} times of breath loop 
        '''

        x_count = 0

        # 主循環，設置 LED 的顏色
        while x_count < c_count0:
            # 從 (0, 0, 0) 到 (255, 0, 0)
            for red in range(max0+1):
                color = (0 << 16) | (red << 8) | 0  # 紅色從 0 遞增到 255，綠色和藍色保持為 0
                self.ar[0] = color
                self.sm.put(self.ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快

            # 從 (0, 0, 0) 到 (255, 0, 0)
            for red in range(max0, -1, -1):
                color = (0 << 16) | (red << 8) | 0  # 紅色從 255 to 0 ，綠色和藍色保持為 0
                self.ar[0] = color
                self.sm.put(self.ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快
            
            # 從 (0, 0, 0) 到 (255, 0, 0)
            for green in range(max0+1):
                color = (green << 16) | (0 << 8) | 0  # 綠色從 0 to 255，紅色保持為 0，藍色保持為 0
                self.ar[0] = color
                self.sm.put(self.ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快

            # 從 (255, 0, 0) 到 (0, 255, 0)
            for green in range(max0, -1, -1):
                color = (green << 16) | (0 << 8) | 0  # 綠色從 255 遞減到 0，紅色保持為 0，藍色保持為 0
                self.ar[0] = color
                self.sm.put(self.ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快
            
            # 從 (0, 255, 0) 到 (0, 0, 255)
            for blue in range(max0+1):
                color = (0 << 16) | (0 << 8) | blue  # 藍色從 0 遞增到 255，紅色和綠色保持為 0
                self.ar[0] = color
                self.sm.put(self.ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快

            # 從 (255, 0, 0) 到 (0, 255, 0)
            for blue in range(max0, -1, -1):
                color = (0 << 16) | (0 << 8) | blue  # 藍色從 255 to 0，紅色和綠色保持為 0
                self.ar[0] = color
                self.sm.put(self.ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快


            # end of while 
            x_count = x_count + 1 
            pass


        pass

    def print_debug(self, content='', always_print0=0):
        '''
        replace the original print function to another debug bus

        '''
        if self.sim_mode == 1 and always_print0 == 1 :
            # real mode change output to the debug bus
            # 240117 change to print all in UART and sim_mcu = 2 allow print to USB COM
            # self.uart1.write(content)
            pass
        elif self.sim_mode == 2:
            # pico connect and need to check termainal
            try: 
                self.uart1.write(content)
            except Exception as e:

                print(f'debug_port_fail{e} at module:{self.module_name}')

            if always_print0 == 1 :
                print(content)
        elif self.sim_mode == 0:
            print(content)
            pass

        pass







if __name__ == '__main__':
    #  the testing code for this file object

    sim_mode = 2 

    led_w = ws2812_LED(sim_mode0=sim_mode)

    testing_index = 2

    if testing_index == 0 : 

        led_w.set_LED0(128)

        pass 

        

    elif testing_index == 1 : 

        while 1 : 

            led_w.breath_type()
            x = input ('enter "y" for exit : ')
            if x == "y":
                break 
        
        pass 

    elif testing_index == 2 : 

        led_w.set_LED()

        

        pass
