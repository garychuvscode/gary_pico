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

# 假设有一个包含多个小于等于255的数字的列表
x_values = [100, 150, 200]

# 将列表直接转换为bytes对象
data_to_write = bytes(x_values)

# 打印结果
print("Data to Write:", data_to_write)

numeric_list = [byte for byte in data_to_write]

print(f"Data to Write, number:{numeric_list}")
