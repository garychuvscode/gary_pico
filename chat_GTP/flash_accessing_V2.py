import uos
import utime


class FlashObj:
    def __init__(self, flash_path="/"):
        self.flash_path = flash_path

    def space_check(self):
        """(function: Check available space on the flash)"""
        try:
            space = uos.statvfs(self.flash_path + "flash")
            total_space = space[0] * space[2]
            free_space = space[0] * space[3]
            return f"Total Space: {total_space} bytes, Free Space: {free_space} bytes"
        except OSError as e:
            return f"Error checking space: {e}"

    def read_file(self, filename):
        """(function: Read the content of a file, parameters: filename - name of the file)"""
        try:
            file_path = f"{self.flash_path}/{filename}"
            with open(file_path, "r") as file:
                content = file.read()
                return content
        except OSError as e:
            return f"Error reading file: {e}"

    def write_file(self, filename, content):
        """(function: Write content to a file, parameters: filename - name of the file, content - content to write)"""
        try:
            file_path = f"{self.flash_path}/{filename}"
            with open(file_path, "w") as file:
                file.write(content)
            return "File written successfully."
        except OSError as e:
            return f"Error writing file: {e}"

    def write_file_append(self, filename, content):
        """(function: Append content to a file, parameters: filename - name of the file, content - content to append)"""
        try:
            file_path = f"{self.flash_path}/{filename}"
            with open(file_path, "a") as file:
                file.write(content)
            return "File appended successfully."
        except OSError as e:
            return f"Error appending file: {e}"

    def write_file_with_separator(self, filename, content, separator="---"):
        """(function: Write content to a file with a separator, parameters: filename - name of the file, content - content to write, separator - separator)"""
        try:
            file_path = f"{self.flash_path}/{filename}"
            with open(file_path, "w") as file:
                file.write(f"{separator} {content} {separator}")
            return "File written with separator successfully."
        except OSError as e:
            return f"Error writing file with separator: {e}"

    def write_file_with_timestamp(self, filename, content):
        """(function: Write content to a file with a timestamp, parameters: filename - name of the file, content - content to write)"""
        try:
            file_path = f"{self.flash_path}/{filename}"
            with open(file_path, "a") as file:
                timestamp = utime.localtime()
                formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
                    timestamp[0],
                    timestamp[1],
                    timestamp[2],
                    timestamp[3],
                    timestamp[4],
                    timestamp[5],
                )
                file.write(f"\n--- New Content ({formatted_time}) ---\n")
                file.write(content)
            return "File written successfully with timestamp."
        except OSError as e:
            return f"Error writing file with timestamp: {e}"

    def list_files(self):
        """(function: List files and directories in the current directory)"""
        try:
            files = uos.listdir(self.flash_path)
            return files
        except OSError as e:
            return f"Error listing files: {e}"

    def remove_directory(self, directory):
        """(function: Recursively remove a directory and its contents, parameters: directory - name of the directory)"""
        try:
            directory_path = f"{self.flash_path}{directory}"
            files = uos.listdir(directory_path)
            for file in files:
                
                file_path = f"{directory_path}/{file}"
                print(f'now is file: {file} in path: {file_path}')
                if (
                    uos.stat(file_path)[0] & 0o170000 == 0o040000
                ):  # Check if it's a directory
                    self.remove_directory(f"{directory}/{file}")
                else:
                    uos.remove(file_path)
                    # add '/' in front of the path : since the root is '/'
                    print(f'remove file: /{file_path} done')
            uos.rmdir(directory_path)
            # add '/' in front of the path : since the root is '/'
            print(f'remove directory: /{directory_path} done')
            return f"Directory '/{directory_path}' removed successfully."
        except OSError as e:
            return f"Error removing directory: {e}"

    def getcwd(self):
        """(function: Get the current working directory)"""
        try:
            current_directory = uos.getcwd()
            print(f'currently in : "{current_directory}"')
            return current_directory
        except OSError as e:
            return f"Error getting current working directory: {e}"


    def find_file_or_directory(self, name, current_path, search_directories=False):
        '''(function: Recursively find file or directory in the given path)'''
        try:
            files = uos.listdir(current_path)
            for file in files:
                file_path = f"{current_path}/{file}"
                if uos.stat(file_path)[0] & 0o170000 == 0o040000:  # Check if it's a directory
                    if search_directories and file == name:
                        return file_path
                    result = self.find_file_or_directory(name, file_path, search_directories)
                    if result:
                        return result
                elif not search_directories and file == name:
                    return file_path
        except OSError as e:
            print(f"Error finding file or directory: {e}")
        return None

    def get_directory_path(self, directory_name):
        '''(function: Get the path of the specified directory in Flash)'''
        result = self.find_file_or_directory(directory_name, self.flash_path, search_directories=True)
        if result:
            return f"The path of directory '{directory_name}' is: {result}"
        else:
            return f"Directory '{directory_name}' not found."

    def interactive_terminal(self):
        '''(function: Interactive terminal for browsing directories and viewing files)'''
        try:
            while True:
                user_input = input("Enter command (exit, dir, file; 'filename', dir; 'directory_name', exit;f): ")
                
                if user_input.startswith("exit"):
                    if user_input == "exit":
                        break
                    elif user_input == "exit;f":
                        return user_input.split(";")[1].strip()

                elif user_input == "dir":
                    try:
                        files = uos.listdir(self.flash_path)
                        print(f"Contents of directory '{self.flash_path}':")
                        for file in files:
                            print(file)
                    except OSError as e:
                        print(f"Error listing directory: {e}")

                elif user_input.startswith("file;"):
                    filename = user_input.split(";")[1].strip()
                    result = self.find_file_or_directory(filename, self.flash_path)
                    if result:
                        try:
                            with open(result, 'r') as file:
                                content = file.read()
                                print(f"Content of file '{result}':\n{content}")
                        except OSError as e:
                            print(f"Error reading file: {e}")
                    else:
                        print(f"File '{filename}' not found.")

                elif user_input.startswith("dir;"):
                    directory_name = user_input.split(";")[1].strip()
                    print(self.get_directory_path(directory_name))

        except KeyboardInterrupt:
            print("\nInteractive terminal aborted.")
# Test FlashObj class functions
flash_obj = FlashObj()

# Test space_check
print(flash_obj.space_check())

# Test read_file
print(flash_obj.read_file("new_file.txt"))

# Test write_file
print(flash_obj.write_file("new_file.txt", "Hello, Flash!"))

# Test write_file_append
print(flash_obj.write_file_append("existing_file.txt", "\nAdditional content."))

# Test write_file_with_separator
print(
    flash_obj.write_file_with_separator(
        "file_with_separator.txt", "Content with separator"
    )
)

# Test write_file_with_timestamp
print(
    flash_obj.write_file_with_timestamp(
        "file_with_timestamp.txt", "Content with timestamp"
    )
)

# Test list_files
print(flash_obj.list_files())

# Test remove_directory
# Create test directories and files
a = "/grace_try1"
try: 
    uos.mkdir(a)
except: 
    print(f'err: {a}')
    pass
b = a + "/grace_try2"
try: 
    uos.mkdir(b)
except: 
    print(f'err: {b}')
    pass
c = b + "/grace_try3"
try: 
    uos.mkdir(c)
except: 
    print(f'err: {c}')
    pass
a = a + '/gary1.txt'
with open(a, "w") as file:
    file.write("Test file 1")
b = b + '/gary2.txt'
with open(b, "w") as file:
    file.write("Test file 2")
c = c + '/gary3.txt'
with open(c, "w") as file:
    file.write("Test file 3")

flash_obj.interactive_terminal()


print(flash_obj.remove_directory("grace_try1"))
# print(flash_obj.remove_directory("grace_try2"))
# print(flash_obj.remove_directory("grace_try3"))

# Test getcwd
print(flash_obj.getcwd())
# Test list_files
print(flash_obj.list_files())
