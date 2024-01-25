import machine
import ustruct

# 初始化 SPI 对象
spi = machine.SPI(
    0,
    baudrate=1000000,
    polarity=0,
    phase=0,
    bits=8,
    sck=machine.Pin(6),
    mosi=machine.Pin(7),
    miso=machine.Pin(4),
)

# 定义要传输的数据
original_data = 0xAA

# 使用 ustruct 将数据反转为 LSB-MSB 传输顺序
reversed_data = ustruct.unpack("B", ustruct.pack("B", original_data)[::-1])[0]

# 传输反转后的数据
spi.write(bytearray([reversed_data]))

# 关闭 SPI 连接
spi.deinit()
