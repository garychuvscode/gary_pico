from machine import Pin, SPI

# spi = SPI(1, 1_000_000)  # Default assignment: sck=Pin(10), mosi=Pin(11), miso=Pin(8)
# spi = SPI(1, 1000000, sck=Pin(14), mosi=Pin(15), miso=Pin(12))
# spi = SPI(0, baudrate=8000000, polarity=0, phase=0, bits=8, sck=Pin(6), mosi=Pin(7), miso=Pin(4))


# spi1 = SPI(0, 1_000_000)  Default assignment: sck=Pin(18), mosi=Pin(19), miso=Pin(16)
spi1 = SPI(0, 1000000, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
spi = SPI(
    1,
    baudrate=8000000,
    polarity=0,
    phase=0,
    bits=8,
    sck=Pin(14),
    mosi=Pin(15),
    miso=Pin(12),
)


# 定义写入的数据
data_to_send = bytearray([0xAA] * 20)  # 使用 0xAA 重复 20 次作为示例数据

# 写入数据到 SPI
spi.write(data_to_send)

# 关闭 SPI 连接
spi.deinit()

"""

=====
>在默認配置下.polarity=0、phase=0 和 bits=8 這些設定通常會使用 SPI 的標準設置。
讓我們將它們解釋一下：

Polarity (polarity):
0:時鐘信號在非活動狀態時為低電平（假設 SCK 線是時鐘信號）。
1:時鐘信號在非活動狀態時為高電平。
在默認配置下.polarity=0 表示 SPI 通信的時鐘信號在非活動狀態時為低電平。

Phase (phase):
0:在時鐘信號的第一個邊緣（上升或下降）開始讀取或寫入數據。
1:在時鐘信號的第二個邊緣讀取或寫入數據。
在默認配置下,phase=0 表示在時鐘信號的第一個邊緣開始讀取或寫入數據。

位數 (bits)
bits=8 表示每個 SPI 傳輸的位數為 8 位。這意味著每次傳輸的數據位數為 8。

總之，默認配置通常是 SPI 的標準配置，時鐘信號在非活動狀態時為低電平，並在時鐘信號的
第一個邊緣開始讀取或寫入 8 位數據。這是一種常見的 SPI 配置，但具體的配置可能取決於
你的硬體和設備的要求。

=====
> SPI(Serial Peripheral Interface)通信的 "bits" 參數表示每個傳輸的位數，
即在一次 SPI 傳輸中每個數據字節的位數。一般而言，可以有不同的 "bits" 選項，例如：

8 位：
bits=8 表示每個傳輸的數據字節有 8 位。這是 SPI 中最常見的配置。
16 位：
bits=16 表示每個傳輸的數據字節有 16 位。在一些應用中，可能需要更長的位數來表示數據。

其他位數：
除了 8 和 16 位之外，一些 SPI 實現還可能支持其他位數的配置，具體取決於硬體和 SPI 控制器的支持情況。
選擇適當的 "bits" 參數取決於你的應用和所連接的 SPI 設備的要求。通常，大多數 SPI 設備都使用 8 位，
但有些特殊應用可能需要更高的精度，因此可能會選擇 16 位。請參閱所使用的具體 SPI
設備的技術規格和文檔，以確定最合適的 "bits" 配置。


=====
Raspberry Pi Pico上的MicroPython提供的machine.SPI类通常支持8、9、16、24和32位的数据传输,
这依赖于硬件的支持。


=====
在 SPI(Serial Peripheral Interface)通信中,CPHA(Clock Phase)和
CPOL(Clock Polarity)是用于定义时钟信号的两个重要参数。

CPHA(Clock Phase):

CPHA 决定数据采样的时机。
CPHA = 0 表示在时钟信号的第一个边沿（上升或下降）开始采样数据。
CPHA = 1 表示在时钟信号的第二个边沿采样数据。
CPOL(Clock Polarity):

CPOL 决定时钟信号的空闲状态。
CPOL = 0 表示在空闲状态时，时钟信号是低电平。
CPOL = 1 表示在空闲状态时，时钟信号是高电平。
这两个参数一起定义了 SPI 总线的时钟极性和相位。
它们的组合决定了数据何时开始传输和何时进行采样。

"""
