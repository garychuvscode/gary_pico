import machine
import time
import json

# 配置GPIO引脚（GP0和GP1）为I2C引脚
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

# I2C设备地址（请根据您的设备地址进行配置）
# control example => 7'h4E = 0x9C
device_address = 0x4E
"""
this is 7 bit address, 0x50 => b01010000
=> change to 8 bit address is b10100000 -> 0xA0
8 bit only used in GPL, so need to know what is real
"""

# 要写入的寄存器地址
register_address = 0xA3

# 要写入的数据
# data_to_write = b"\x01\x02\x03"
data_to_write = b"\x01"

test_mode = 3

if test_mode == 1:
    # testing for number input scan from 0-255
    x = 0
    while 1:
        if x == 256:
            x = 0
        # write from 0-255
        print(f"now counter is {x}")
        data_to_write = f"{hex(x)[2:]}"
        data_to_write = data_to_write.encode("utf-8")
        print(f"data read to wirte: {data_to_write}")
        # data_to_write = b"\x01"
        # 使用i2c.writeto_mem()写入数据到指定寄存器位置
        # i2c.writeto_mem(device_address, register_address, data_to_write)
        time.sleep(0.05)

        x = x + 1

if test_mode == 2:
    # command transfer
    def convert_to_hex(number, input_format="dec"):
        if input_format == "dec":
            number = int(number)
            if 0 <= number <= 255:
                return hex(number)[2:]
            else:
                raise ValueError("Input number must be in the range 0 to 255.")
        elif input_format == "hex":
            # 如果输入已经是十六进制字符串，直接返回
            return number
        else:
            raise ValueError("Invalid input_format. Use 'dec' or 'hex'.")

    while 1:
        print(f"PICO say hi to Grace~ ")
        cmd = input()
        cmd_s = cmd.split(";")
        res = convert_to_hex(number=cmd_s[0], input_format=str(cmd_s[1]))
        print(f"input: {cmd}, number: {cmd_s[0]}, type: {cmd_s[1]}")
        print(f"Dear Grace, please send I2C data: {res}")

    # 示例用法：
    decimal_input = 42
    hex_result = convert_to_hex(decimal_input)
    print(f"Decimal {decimal_input} in hex: {hex_result}")

    hex_input = "0x2a"
    hex_result = convert_to_hex(hex_input, input_format="hex")
    print(f"Hex {hex_input} without '0x': {hex_result}")

if test_mode == 3:
    # write testing
    x = 0
    while 1:
        if x == 256:
            x = 0
        # write from 0-255
        print(f"now counter is {x}, which is {hex(x)[2:]} in hex")
        data_to_write = bytes([x, x + 1, x + 2])
        # data_to_write = data_to_write.encode("utf-8")
        print(f"data read to wirte: {data_to_write}")

        i2c.writeto_mem(device_address, register_address, data_to_write)
        print(f"write done")

        time.sleep(0.2)
        # 发送要读取的寄存器地址
        i2c.writeto(device_address, bytes([register_address]))
        # 从I2C设备读取数据
        data = i2c.readfrom(device_address, 1)  # 4表示要读取的字节数

        # 打印读取的数据
        print("data read from the bus:", data)

        # time.sleep(10)
        input()
        x = x + 1
