import uos
import utime


class FlashObj:
    def __init__(self, flash_path="/"):
        self.flash_path = flash_path
        self.sim_flash = 0

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

    def write_file(self, filename, content, type0="w"):
        """(function: Write content to a file, parameters: filename - name of the file, content - content to write)"""
        try:
            file_path = f"{self.flash_path}/{filename}"
            with open(file_path, type0) as file:
                file.write(content)
            return "File written successfully."
        except OSError as e:
            return f"Error writing file: {e}"

    def write_file_append(self, filename, content, type0="a"):
        """(function: Append content to a file, parameters: filename - name of the file, content - content to append)"""
        try:
            file_path = f"{self.flash_path}/{filename}"
            with open(file_path, type0) as file:
                file.write(content)
            return "File appended successfully."
        except OSError as e:
            return f"Error appending file: {e}"

    def write_file_with_separator(self, filename, content, separator="---", type0="w"):
        """(function: Write content to a file with a separator, parameters: filename - name of the file, content - content to write, separator - separator)"""
        try:
            file_path = f"{self.flash_path}/{filename}"
            with open(file_path, type0) as file:
                file.write(f"{separator} {content} {separator}")
            return "File written with separator successfully."
        except OSError as e:
            return f"Error writing file with separator: {e}"

    def write_file_with_timestamp(self, filename, content, type0="a"):
        """(function: Write content to a file with a timestamp, parameters: filename - name of the file, content - content to write)"""
        try:
            file_path = f"{self.flash_path}/{filename}"
            with open(file_path, type0) as file:
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
                print(f"now is file: {file} in path: {file_path}")
                if (
                    uos.stat(file_path)[0] & 0o170000 == 0o040000
                ):  # Check if it's a directory
                    self.remove_directory(f"{directory}/{file}")
                else:
                    uos.remove(file_path)
                    # add '/' in front of the path : since the root is '/'
                    print(f"remove file: /{file_path} done")
            uos.rmdir(directory_path)
            # add '/' in front of the path : since the root is '/'
            print(f"remove directory: /{directory_path} done")
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

    def find_file_or_directory(self, name, current_path="/", print0=1):
        try:
            files = uos.listdir(current_path)
            # print(f"we have: {files}")
            for file in files:
                file_path = f"{current_path}/{file}"
                # print(f"check path {file_path}")
                # check if the name match
                if file == name:
                    # founded the result and return
                    return file_path
                else:
                    is_directory = uos.stat(file_path)[0] & 0o170000 == 0o040000
                    if is_directory:
                        # Recursive call for directories
                        result = self.find_file_or_directory(name, file_path, print0=0)
                        if result:
                            return result

            if print0 == 1:
                print(f"oh no~ there is no such things {name} XDD")

        except OSError as e:
            print(f"Error finding file or directory: {e}")

        return None

    def get_directory_path(self, directory_name):
        """(function: Get the path of the specified directory in Flash)"""
        result = self.find_file_or_directory(directory_name, self.flash_path)
        if result:
            return f"The path of directory '{directory_name}' is: {result}"
        else:
            return f"Directory '{directory_name}' not found."

    def interactive_terminal(self):
        """
        (function: Interactive terminal for browsing directories and viewing files)
        """
        try:
            while True:
                print(f"now in flash operating terminal")
                user_input = input(
                    "Enter command (exit, dir, file;'filename', dir;'directory_name', cmd;'cmd_str', cdir;'directory_name', cname;'old_name';'new_name', list_all): "
                )

                if user_input.startswith("exit"):
                    if user_input == "exit":
                        break

                elif user_input == "dir":
                    try:
                        dir_now = uos.getcwd()
                        files = uos.listdir(dir_now)
                        print(f"Contents of directory '/{dir_now}':")
                        for file in files:
                            print(file)
                    except OSError as e:
                        print(f"Error listing directory: {e}")

                elif user_input.startswith("file;"):
                    filename = user_input.split(";")[1].strip()
                    result = self.find_file_or_directory(filename, self.flash_path)
                    if result:
                        try:
                            with open(result, "r") as file:
                                content = file.read()
                                print(f"Content of file '{result}':\n{content}")
                        except OSError as e:
                            print(f"Error reading file: {e}")
                    else:
                        print(f"File '{filename}' not found.")

                elif user_input.startswith("dir;"):
                    try:
                        directory_name = user_input.split(";")[1].strip()
                        print(self.get_directory_path(directory_name))
                    except OSError as e:
                        print(f"Error : {e}")

                elif user_input.startswith("cmd;"):
                    try:
                        command = user_input.split(";")[1].strip()
                        print(self.str_to_code(command))
                    except OSError as e:
                        print(f"Error : {e}")

                elif user_input.startswith("cdir;"):
                    try:
                        command = user_input.split(";")[1].strip()
                        self.c_dir(command)

                    except OSError as e:
                        print(f"Error change dir : {e}")

                elif user_input.startswith("cname;"):
                    try:
                        old_path0 = user_input.split(";")[1].strip()
                        new_path0 = user_input.split(";")[2].strip()
                        uos.rename(old_path0, new_path0)

                    except OSError as e:
                        print(f"Error change dir : {e}")

                elif user_input.startswith("list_all;"):
                    try:
                        self.list_all_files()

                    except OSError as e:
                        print(f"Error change dir : {e}")

        except KeyboardInterrupt:
            print("\nInteractive terminal aborted.")

    def c_dir(self, target_dir_name):
        """
        search the directory, print out the file path, and change to the related
        directory
        """
        # looking for the directory from the root (default current path)
        full_path0 = "/"
        if target_dir_name != "/":
            full_path0 = self.find_file_or_directory(name=target_dir_name)
            uos.chdir(full_path0)
        else:
            uos.chdir("/")

        print(f"now change to {uos.getcwd()}")

        return full_path0

    def str_to_code(self, string0="", *args, **kwargs):
        """
        function run for string command, also include the adjustment of 'TAB'
        to prevent error for the operation
        """
        # # 231114, this is just testing string for the debugging
        # string0 = '''self.print_debug(content=f'Grace went back home now', always_print0=1)'''

        # 231114: add the reference dictionary to the exec function
        self.str_code_ref = {"self": self}
        # merge the self object with kwargs for cute Grace
        self.str_code_ref.update(kwargs)

        try:
            # string0 = str(string0)
            # textwrap => can't be used, give up and just for record
            # string0 = textwrap.dedent(string0)

            # there seems to have error
            string0 = self.dedent(string0)
            # res = exec(string0, globals(), self.str_code_ref)
            # 24011 for the operation needed to have return, use eval
            # to replace exec, exec is only have excution
            res = eval(string0, globals(), self.str_code_ref)
            return res
            # self.execute_indented_code(string0)
        except Exception as e:
            self.print_debug(f"exception: {e}", always_print0=1)
            # 231114: watchout! don't use try-except too early
            # or you may not see the issue
            self.print_debug(
                content=f"there are some issue of exec() \n with string \n{string0}",
                always_print0=1,
            )
        pass

    def dedent(self, code):
        lines = code.split("\n")
        # 计算最小缩进
        min_indent = float("inf")
        for line in lines:
            stripped = line.lstrip()
            if stripped:
                indent = len(line) - len(stripped)
                min_indent = min(min_indent, indent)

        # 移除最小缩进
        dedented_lines = [line[min_indent:] for line in lines]
        dedented_code = "\n".join(dedented_lines)
        return dedented_code

    def print_debug(self, content="", always_print0=0):
        """
        for the flash check only sim = 0 need to print
        """
        if self.sim_flash == 0:
            print(content)
            pass

        pass

    def list_all_files(self, directory="/", result=[], print0=1):
        """Recursively list all files in the specified directory"""
        try:
            files = uos.listdir(self.flash_path + directory)
            # print(files)
            # result = []
            for file in files:
                file_path = f"{self.flash_path}{directory}/{file}"
                if uos.stat(file_path)[0] & 0o170000 == 0o040000:
                    # Check if it's a directory
                    # result.append(f"{indent}{file}/")
                    # Recursive call to list files in the subdirectory
                    self.list_all_files(f"{directory}/{file}", result=result, print0=0)
                else:
                    result.append(f"{directory}/{file}")

            if print0 == 1:
                print(f"now is going to print all the file: \n")
                for i in result:
                    print(i)
                    pass
                # gjust give another line to separate in the terminal
                print()
            return result
        except OSError as e:
            return [f"Error listing files: {e}"]


# Test FlashObj class functions
flash_obj = FlashObj()

if __name__ == "__main__":
    # testing code of flsh_obj

    # Test space_check
    print(flash_obj.space_check())

    flash_obj.list_all_files()

    # Test write_file
    print(flash_obj.write_file("new_file.txt", "Hello, Flash!"))

    # Test read_file
    print(flash_obj.read_file("new_file.txt"))

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
        print(f"err: {a}")
        pass
    b = a + "/grace_try2"
    try:
        uos.mkdir(b)
    except:
        print(f"err: {b}")
        pass
    c = b + "/grace_try3"
    try:
        uos.mkdir(c)
    except:
        print(f"err: {c}")
        pass
    a = a + "/gary1.txt"
    with open(a, "w") as file:
        file.write("Test file 1")
    b = b + "/gary2.txt"
    with open(b, "w") as file:
        file.write("Test file 2")
    c1 = c + "/gary3.txt"
    with open(c1, "w") as file:
        file.write("Test file 3")
    c2 = c + "/gary4.txt"
    with open(c2, "w") as file:
        file.write("Test file 4")

    flash_obj.list_all_files()

    # this need to be full path or just under current directory
    # uos.chdir("grace_try2")
    uos.chdir("/grace_try1")

    flash_obj.interactive_terminal()

    # print(flash_obj.remove_directory("grace_try1"))
    # print(flash_obj.remove_directory("grace_try2"))
    # print(flash_obj.remove_directory("grace_try3"))

    # Test getcwd
    print(flash_obj.getcwd())
    # Test list_files
    print(flash_obj.list_files())
