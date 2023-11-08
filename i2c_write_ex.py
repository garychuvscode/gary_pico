import machine

# 配置GPIO引脚（GP0和GP1）为I2C引脚
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))

# I2C设备地址（请根据您的设备地址进行配置）
device_address = 0x50
"""
this is 7 bit address, 0x50 => b01010000
=> change to 8 bit address is b10100000 -> 0xA0
8 bit only used in GPL, so need to know what is real
"""

# 要写入的寄存器地址
register_address = 0x10

# 要写入的数据
data_to_write = b"\x01\x02\x03"

# 使用i2c.writeto_mem()写入数据到指定寄存器位置
i2c.writeto_mem(device_address, register_address, data_to_write)

print("数据已写入到指定寄存器位置")
