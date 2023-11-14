# 假设有一个bytes对象
data_bytes = b"\x41\x42\x43"

# 将每个字节转换为独立的数字列表
numeric_list = [byte for byte in data_bytes]

# 打印结果
print("Numeric List:", numeric_list)

data_bytes = numeric_list[0]
print(f"{data_bytes}")

# # =====

# data_bytes = b"\x41\x42\x43"
# # 将bytes对象转换为十进制
# dec_value = int.from_bytes(data_bytes, "big")

# # 将bytes对象转换为十六进制
# hex_value = hex(int.from_bytes(data_bytes, "big"))

# # 打印结果
# print("Decimal:", dec_value)
# print("Hexadecimal:", hex_value)

# # =====
