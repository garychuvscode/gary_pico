import uos


stat = uos.statvfs("/flash")

flash_path = "/flash"

# 获取Flash的总大小、已使用的空间和剩余的空间
total_space = stat[0] * stat[2]  # stat[0] 是块大小，stat[2] 是块总数
free_space = stat[0] * stat[3]  # stat[3] 是剩余块数
used_space = total_space - free_space

print(f"Flash size: {total_space} byte")
print(f"used: {used_space} byte")
print(f"left: {free_space} byte")

space_info = [total_space, free_space]

name = uos.uname()
print(f'name: "{name}" \n')

root_dir = uos.getcwd()
print(f'current directly: "{root_dir}" \n')

root_list = uos.listdir(root_dir)
print(f'we have: "{root_list}" \n')


# # 指定新目录的路径
new_directory_path = "/grace_try"

try:
    # 使用 uos.mkdir 创建新目录
    uos.mkdir(new_directory_path)
    print(f"Directory '{new_directory_path}' created successfully.")
except OSError as e:
    print(f"Error creating directory: {e}")

filename = "gary_is_here.txt"
content = "gary say hi to grace"

file_path = f"{new_directory_path}/{filename}"
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

    print(f"File written successfully.")
except OSError as e:
    print(f"Error writing file: {e}")

new_directory_path2 = new_directory_path + "/grace_try2"

try:
    # 使用 uos.mkdir 创建新目录
    uos.mkdir(new_directory_path2)
    print(f"Directory '{new_directory_path2}' created successfully.")
except OSError as e:
    print(f"Error creating directory: {e}")

filename = "gary_is_here2.txt"
content = "gary say hi to grace2"

file_path = f"{new_directory_path2}/{filename}"
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

    print(f"File written successfully {filename}.")
except OSError as e:
    print(f"Error writing file: {e}")


file_path = f"{new_directory_path2}/{filename}"
print(f"path contain: {uos.listdir(new_directory_path)}")

try:
    with open(file_path, "r") as file:
        content = file.read()
        print(content)
except OSError as e:
    print(f"Error reading file: {e}")

root_list = uos.listdir(root_dir)
print(f'we have: "{root_list}" \n')

# uos.rmdir(new_directory_path)


def remove_directory(path):
    try:
        # 列出目录中的所有文件和子目录
        files = uos.listdir(path)

        # 删除目录中的文件和子目录
        for file in files:
            file_path = path + "/" + file  # 使用字符串拼接构建文件路径
            if uos.stat(file_path)[0] & 0o170000 == 0o040000:  # 判断是否为目录
                # 递归删除子目录
                remove_directory(file_path)
            else:
                # 删除文件
                uos.remove(file_path)

        # 删除空的目录
        uos.rmdir(path)
        print(f"Directory '{path}' removed successfully.")
    except OSError as e:
        print(f"Error removing directory: {e}")


# 示例：删除非空目录
remove_directory(new_directory_path)


root_list = uos.listdir(root_dir)
print(f'we have: "{root_list}" \n')
