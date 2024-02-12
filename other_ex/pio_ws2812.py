import array
import time
from machine import Pin
import rp2

# 設置要控制的 WS2812 LED 的數量
NUM_LEDS = 1

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
sm = rp2.StateMachine(1, ws2812, freq=8_000_000, sideset_base=Pin(23))

# 啟動 StateMachine，準備接收 FIFO 中的數據
sm.active(1)

# 創建 array 來存儲 LED 的顏色數據 ('I' is )第一個參數 "I" 指定了數組中元素的類型，
# 這裡的 "I" 表示每個元素都是一個無符號整數（即正整數），第二個參數 [0] 是一個列表，
# 包含了初始值為 0 的一個元素，所以這個數組就只包含一個整數 0。
ar = array.array("I", [0])




if __name__ == '__main__':
    #  the testing code for this file object



    testing_index = 0

    if testing_index == 0 : 

        # 主循環，設置 LED 的顏色
        while True:
            # 對於每一顆 LED
            for led_index in range(NUM_LEDS):
                # 根據給定的紅、綠和藍值，計算出顏色數據
                red = int(input(f"Enter red value for LED {led_index + 1} (0-255): "))
                green = int(input(f"Enter green value for LED {led_index + 1} (0-255): "))
                blue = int(input(f"Enter blue value for LED {led_index + 1} (0-255): "))
            
                # 將紅、綠、藍值組合成一個顏色數據，按照 WS2812 的順序排列
                color = (green << 16) | (red << 8) | blue
                
                # 將顏色數據放入 array 中
                ar[led_index] = color
                print(ar)
            
            # 將 array 放入 StateMachine 的 FIFO 中，從而將顏色數據發送到 WS2812 LED
            sm.put(ar, 8)
            
            # 等待一段時間，以便觀察 LED 的顏色
            time.sleep_ms(50)

    if testing_index == 1 : 
        
        # 主循環，設置 LED 的顏色
        while True:
            # 從 (0, 0, 0) 到 (255, 0, 0)
            for red in range(256):
                color = (0 << 16) | (red << 8) | 0  # 紅色從 0 遞增到 255，綠色和藍色保持為 0
                ar[0] = color
                sm.put(ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快

            # 從 (0, 0, 0) 到 (255, 0, 0)
            for red in range(255, -1, -1):
                color = (0 << 16) | (red << 8) | 0  # 紅色從 255 to 0 ，綠色和藍色保持為 0
                ar[0] = color
                sm.put(ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快
            
            # 從 (0, 0, 0) 到 (255, 0, 0)
            for green in range(256):
                color = (green << 16) | (0 << 8) | 0  # 綠色從 0 to 255，紅色保持為 0，藍色保持為 0
                ar[0] = color
                sm.put(ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快

            # 從 (255, 0, 0) 到 (0, 255, 0)
            for green in range(255, -1, -1):
                color = (green << 16) | (0 << 8) | 0  # 綠色從 255 遞減到 0，紅色保持為 0，藍色保持為 0
                ar[0] = color
                sm.put(ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快
            
            # 從 (0, 255, 0) 到 (0, 0, 255)
            for blue in range(256):
                color = (0 << 16) | (0 << 8) | blue  # 藍色從 0 遞增到 255，紅色和綠色保持為 0
                ar[0] = color
                sm.put(ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快

            # 從 (255, 0, 0) 到 (0, 255, 0)
            for blue in range(255, -1, -1):
                color = (0 << 16) | (0 << 8) | blue  # 藍色從 255 to 0，紅色和綠色保持為 0
                ar[0] = color
                sm.put(ar, 8)
                time.sleep_ms(10)  # 等待一小段時間，使顏色變化不要太快

    elif testing_index == 2 : 

        '''
        這樣，程式將進行從黑色 (0, 0, 0) 到白色 (255, 255, 255)，
        然後再從白色回到黑色的循環，同時每個顏色的亮度都會逐漸增加和減少。
        '''


        # 主循環，設置 LED 的顏色
        while True:
            # 從 (0, 0, 0) 到 (255, 255, 255)
            for color_value in range(256):
                for color_offset in range(256):
                    red = color_value if color_offset <= color_value else 255 - color_offset
                    green = color_value if color_offset <= color_value else 255 - color_offset
                    blue = color_value if color_offset <= color_value else 255 - color_offset
                    color = (green << 16) | (red << 8) | blue
                    ar[0] = color
                    sm.put(ar, 8)
                    time.sleep_ms(30)  # 等待一小段時間，使顏色變化不要太快
            
            # 從 (255, 255, 255) 到 (0, 0, 0)
            for color_value in range(255, -1, -1):
                for color_offset in range(256):
                    red = color_value if color_offset <= color_value else 255 - color_offset
                    green = color_value if color_offset <= color_value else 255 - color_offset
                    blue = color_value if color_offset <= color_value else 255 - color_offset
                    color = (green << 16) | (red << 8) | blue
                    ar[0] = color
                    sm.put(ar, 8)
                    time.sleep_ms(30)  # 等待一小段時間，使顏色變化不要太快
