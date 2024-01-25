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


rx_data = bytearray(64)  # 初始化为 64 个零字节

# reset the RX array before reading new data
for i in range(len(rx_data)):
    rx_data[i] = 0

# 240125 there is no fill function in micro python
# # 在每次读取之前将 rx_data 初始化为零
# rx_data.fill(0)
spi.readinto(rx_data)
