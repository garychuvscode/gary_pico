import machine

# 配置GPIO引脚（GP0和GP1）为I2C引脚
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))

# I2C设备地址（请根据您的设备地址进行配置）
# control example => 7'h4E = 0x9C
device_address = 0x4E
"""
this is 7 bit address, 0x50 => b01010000
=> change to 8 bit address is b10100000 -> 0xA0
8 bit only used in GPL, so need to know what is real
"""

# 要读取的寄存器地址
register_address = 0xA1

# 发送要读取的寄存器地址
i2c.writeto(device_address, bytes([register_address]))

# 从I2C设备读取数据
data = i2c.readfrom(device_address, 4)  # 4表示要读取的字节数

# 打印读取的数据
print("读取的数据:", data)
