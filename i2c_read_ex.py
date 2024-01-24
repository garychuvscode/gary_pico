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
register_address = 0xA0

# 发送要读取的寄存器地址
i2c.writeto(device_address, bytes([register_address]))

# 从I2C设备读取数据
data = i2c.readfrom(device_address, 48)  # 4表示要读取的字节数
# 將每個字節轉換為十六進制字符串，並使用逗號分隔
hex_strings = ", ".join([hex(byte) for byte in data])

# 打印读取的数据
print(f" data_get: {repr(hex_strings)} ")
# print("data_get:", data)

# 去除 "0x" 並分割字符串
hex_values = hex_strings.replace("0x", "").split(", ")

# # 將每個字符串轉換為十進制整數，再轉換為沒有 "0x" 的十六進制字符串
# byte_list = [hex(int(value, 16))[2:] for value in hex_values]

# 將每個字符串轉換為十進制整數，再轉換為固定兩位的十六進制字符串
byte_list = ["{:02X}".format(int(value, 16)) for value in hex_values]

# 打印結果
print("byte_list:", byte_list)

print(f" final byte: {byte_list[3]} ")
