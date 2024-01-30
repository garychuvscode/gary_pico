# fmt: off

import uos
import utime

# 获取Flash文件系统的统计信息
stat = uos.statvfs("/flash")

# 获取Flash的总大小、已使用的空间和剩余的空间
total_space = stat[0] * stat[2]  # stat[0] 是块大小，stat[2] 是块总数
free_space = stat[0] * stat[3]  # stat[3] 是剩余块数
used_space = total_space - free_space

print(f"Flash size: {total_space} byte")
print(f"used: {used_space} byte")
print(f"left: {free_space} byte")

class FlashObj:
    def __init__(self, flash_path="/flash"):
        self.flash_path = flash_path

    def space_check(self):
        stat = uos.statvfs("/flash")

        # 获取Flash的总大小、已使用的空间和剩余的空间
        total_space = stat[0] * stat[2]  # stat[0] 是块大小，stat[2] 是块总数
        free_space = stat[0] * stat[3]  # stat[3] 是剩余块数
        used_space = total_space - free_space

        print(f"Flash size: {total_space} byte")
        print(f"used: {used_space} byte")
        print(f"left: {free_space} byte")

        space_info = [total_space, free_space]

        return space_info

    def read_file(self, filename):
        file_path = f"{self.flash_path}/{filename}"
        try:
            with open(file_path, "r") as file:
                content = file.read()
                return content
        except OSError as e:
            return f"Error reading file: {e}"

    def write_file(self, filename, content):
        file_path = f"{self.flash_path}/{filename}"
        try:
            with open(file_path, "w") as file:
                file.write(content)

                """
                在示例代码中write_file 方法使用的是Python内置的 open 函数，其中使
                用了 'w' 模式，表示以写入方式打开文件。如果文件已经存在，则该方法会覆盖
                文件内容；如果文件不存在，则会创建新文件。
                所以，如果调用 write_file 方法时指定的文件名已存在，它将会被覆盖
                并写入新的内容。如果文件名不存在，它会创建一个新的文件并写入内容。
                如果你希望在文件已经存在时追加内容而不是覆盖，可以使用 'a' 模式。
                """

            return "File written successfully."
        except OSError as e:
            return f"Error writing file: {e}"

    def write_file_append(self, filename, content):
        file_path = f"{self.flash_path}/{filename}"
        try:
            with open(file_path, "a") as file:
                file.write(content)
            return "File written successfully (append)."
        except OSError as e:
            return f"Error writing file: {e}"

    def write_file_with_separator(self, filename, content):
        file_path = f"{self.flash_path}/{filename}"
        try:
            with open(file_path, "a") as file:
                file.write("\n--- New Content ---\n")
                file.write(content)
            return "File written successfully with separator."
        except OSError as e:
            return f"Error writing file: {e}"

    def write_file_with_timestamp(self, filename, content):
        file_path = f"{self.flash_path}/{filename}"
        try:
            with open(file_path, 'a') as file:
                timestamp = utime.localtime()
                formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
                    timestamp[0], timestamp[1], timestamp[2],
                    timestamp[3], timestamp[4], timestamp[5]
                )
                file.write(f"\n--- New Content ({formatted_time}) ---\n")
                file.write(content)
            return "File written successfully with timestamp."
        except OSError as e:
            return f"Error writing file: {e}"

    def list_files(self):
        try:
            files = uos.listdir(self.flash_path)
            return files
        except OSError as e:
            return f"Error listing files: {e}"


# 创建 FlashObj 的实例
flash_obj = FlashObj()

# 示例：写入文件
write_result = flash_obj.write_file("new_file.txt", "Hello, Flash1!")
print(write_result)

# 示例：读取文件
content = flash_obj.read_file("example.txt")
print("Content of example.txt:", content)

# 示例：写入文件
write_result = flash_obj.write_file("new_file.txt", "Hello, Flash!")
print(write_result)

content = flash_obj.read_file("new_file.txt")
print("the result after write_file :", content)

# 示例：追加内容
append_result = flash_obj.write_file_append("new_file.txt", "This is appended content.")
print(append_result)

content = flash_obj.read_file("new_file.txt")
print("the result after write_file_append :", content)


# 示例：带有分隔符的追加
separator_result = flash_obj.write_file_with_separator(
    "new_file.txt", "New content with separator."
)
print(separator_result)

content = flash_obj.read_file("new_file.txt")
print("the result after write_file_with_separator :", content)

# 示例：带有时间戳的追加
timestamp_result = flash_obj.write_file_with_timestamp(
    "new_file.txt", "New content with timestamp."
)
print(timestamp_result)

content = flash_obj.read_file("new_file.txt")
print("the result after write_file_with_timestamp :", content)

# 示例：列出文件
file_list = flash_obj.list_files()
print("Files in Flash:", file_list)
