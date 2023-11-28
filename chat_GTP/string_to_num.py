# 原始字符串
original_string = "i2c;w;addr;[1,2,3,4,5]"

# 使用分號分割字符串
split_parts = original_string.split(";")

# 提取包含整數的字符串，即 '[1,2,3,4,5]'
integer_string = split_parts[-1]

# 使用負數索引時，-1 表示列表的最後一個元素，-2 表示倒數第二個元素，以此類推。這是 Python 中常見的索引運算方式。


# 使用 eval 函數將字符串轉換為列表
integer_list = eval(integer_string)
integer_list_b = bytes(integer_list)


# 打印結果
print(integer_list)
