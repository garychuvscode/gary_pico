import os
import subprocess

# # also for the jump out window, same group with win32con
import win32api
from win32con import MB_SYSTEMMODAL
import pyvisa
import re


# pyvisa only support 9600 baud rate, use serial for higher baudrate
rm = pyvisa.ResourceManager()


class PicoBridge:
    def __init__(self):
        """
        bridging with the pico, PC ad Pico
        """
        # default com_address:
        self.com_addr = "COM4"
        self.sim_mcu = 1
        self.com_index = 1

        # using the COM open to fine the correct device
        pass

    def com_open(self, open=0):
        """
        231112: no need to change the baud rate, default should be enough
        PICO use just like genetal communication method like input() of python
        """
        # this function is used to open the com port of the MCU
        # this will be set independentlly in each object
        print("now the COM port of PICO is on")
        uart_cmd_str = f"COM{self.com_addr}"
        print(uart_cmd_str)
        if self.sim_mcu == 1:
            check_ID = ""
            while 1:
                # 240117 add new operation: clear the resource for reset
                list_dev = rm.list_resources()
                print(f"the related resource we have \n {list_dev}")
                try:
                    # first use the default value
                    self.mcu_com = rm.open_resource(uart_cmd_str)
                    check_ID = self.p_query(cmd_str0="*IDN?")
                    print(f"MCU ID_check finished, pico and {check_ID}")
                    # 240128: use try to check if the resource open ok

                    # for the connection speed, at least use 115200, there
                    # are time out issue if the frequency is too slow
                    if check_ID == "Grace":
                        print(f"correct and break")
                        break
                    else:
                        print(f"ID not correct")
                        raise Exception("ID not correct")  # 使用 raise 引发异常

                except Exception as e:
                    # search from all USB device
                    print(f"input ID not found, enter univeral search")
                    available_devices = rm.list_resources()

                    for device in available_devices:
                        print(f"now test: {device} ")
                        try:
                            # to check what is pico
                            self.mcu_com = rm.open_resource(str(device))
                            self.mcu_com.clear()
                            self.mcu_com.write("*IDN?")
                            # the first of read in pico after write is to get command
                            cmd_write = self.mcu_com.read()
                            # the second read is the return item (if there are return)
                            item_back = self.mcu_com.read()
                            check_ID = item_back.strip()
                            print(item_back)
                            print(
                                f"what we got on usb is: first the command {cmd_write},second the item_back {item_back}"
                            )
                            if check_ID == "Grace":
                                print(f"correct and break")
                                # this break if active for the for loop

                                # also assign the correct COM address for reference
                                self.com_addr = str(device)
                                self.com_index = f'COM{self.extract_numeric_part(self.com_addr)}'
                                break

                        except Exception as e:
                            # may not have or wrong device
                            print(f"exception: {e}, please check pico connection")
                            pass

                        # end of check device for loop
                        pass

                    if check_ID == "Grace":
                        print(f"correct and break")
                        break
                    # end of the external exception
                    pass

                if check_ID != "Grace":
                    self.message_box(
                        content_str=f'the ID: "{check_ID}" is wrong, check PCIO MCU connection',
                        title_str="MCU not found",
                    )
                # end of while
                pass

        else:
            print("open COM port but bypass the real operation")

        if open == 0 : 
            # pico bridge mode, need to close COM port
            # because ampy need to access COM, don't be occupied 
            # by resource manager 
            self.com_close()
            print(f'the com index is: {self.com_index}')

        pass

    def p_query(self, cmd_str0="t;usb;2", time_out_s0=5):
        """
        command send and looking for feedback => used for
        data return of checking the feedback of command
        send to PICO(double check)
        test_LED 2 => GP9
        240124: better to clear the COM port RX FIFO before query
        to get the latet information => using read or clear
        """

        if self.sim_mcu == 1:
            try:
                # try to read out all the stuff first
                tmp_r = self.mcu_com.read()
                print(f"first to clear FIFO: {tmp_r}")

            except Exception as e:
                print(f"FIFO is empty or other error: {e}")

            try:
                # then start query
                tmp_cmd = self.mcu_com.query(cmd_str0, time_out_s0)
                # 240128 add one more offset for the read offset
                tmp_r = self.mcu_com.read()
                tmp_r = tmp_r.strip()
                print(f"pico repeat item send: {tmp_cmd}, result back: {tmp_r}")
                return tmp_r
                pass
            except Exception as e:
                print(f"query error, need to check command with error: {e}")
                pass

            pass
        else:
            print(f"PICO sim_mode query {cmd_str0}")

        # end of query
        pass

    def p_write(self, command="t;usb;5"):
        """
        run the command and without return
        only try to print the result
        test_LED 5 => GP22
        240124 watch out that the old commend send to PICO will be
        save in the FIFO buffer if sending command faster than
        excuting
        """
        ret_from_pico = 0
        try:
            if self.sim_mcu == 1:
                ret_from_pico = self.mcu_com.write(command)
                # ret_from_pico = self.mcu_com.query(command)
            else:
                ret_from_pico = f"sim_mode_{command}"
            print(f"Grace is about 30y, and she say: {ret_from_pico}")
        except Exception as e:
            print(f'write error "{e}" at address{self.com_addr}')

        pass

    def com_close(self):
        # after the verification is finished, reset all the condition
        # to initial and turn off the communication port

        print("the MCU will turn off")
        if self.sim_mcu == 1:
            self.mcu_com.close()
        else:
            print("the com port is turn off now")

        pass

    def message_box(self, content_str, title_str, box_type=0):
        """
        message box function
        auto_exception is for waveform capture, will bypass fully auto setting in global setting \n
        boxtype(mpaaed with return value): 0-only confirm\n
        1-confirm: 1, cancel: 2
        2-stop: 3, re-try: 4, skip: 5
        3-yes: 6, no: 7, cancel: 2
        4-yes: 6, no: 7
        """
        content_str = str(content_str)
        title_str = str(title_str)
        msg_res = 7
        # won't skip if not enter the result update
        msg_res = win32api.MessageBox(0, content_str, title_str, box_type)
        # 0 to 3 is different type of message box and can sen different return value
        # detail check on the internet
        print("msg box call~~ ")
        print("P.S Grace is cute! ~ ")

        return msg_res
    
    def extract_numeric_part(self, address):
        """
        Extracts the numeric part from a given address.

        Parameters:
        address (str): The address string containing numeric and non-numeric parts.

        Returns:
        str: The numeric part extracted from the address.
        """
        try:
            numeric_part = re.search(r'\d+', address).group()
            return numeric_part
        except Exception as e:
            print(f'Error: {e}')

    def execute_commands(self, commands):
        """執行一系列系統命令"""
        for command in commands:
            process = subprocess.run(
                command, shell=True, capture_output=True, text=True
            )
            if process.returncode == 0:
                print(f"命令 '{command}' 執行成功:")
                print(process.stdout)
            else:
                print(f"命令 '{command}' 執行失敗:")
                print(process.stderr)

    def make_dir(self, file_dir):
        """
        Create directories recursively on Pico.

        Args:
            file_dir (str): The directory path to be created.
        """
        try:
            dirs = file_dir.split("/")
            for d in dirs:
                subprocess.run(["ampy", "--port", "/dev/ttyACM0", "mkdir", d])
        except Exception as e:
            print(f"Error: {e}")

    def del_dir(self, file_dir):
        """
        Delete directory and its contents on Pico.

        Args:
            file_dir (str): The directory path to be deleted.
        """
        try:
            subprocess.run(["ampy", "--port", "/dev/ttyACM0", "rmdir", file_dir])
        except Exception as e:
            print(f"Error: {e}")

    def input_to_pico(self, file_dir):
        """
        Transfer files from computer to Pico.

        Args:
            file_dir (str): The directory path on the computer.
        """
        try:
            self.make_dir(file_dir)
            for root, dirs, files in os.walk(file_dir):
                for f in files:
                    file_path = os.path.join(root, f)
                    rel_path = os.path.relpath(file_path, file_dir)
                    pico_path = os.path.join("/", rel_path)
                    subprocess.run(
                        ["ampy", "--port", "/dev/ttyACM0", "put", file_path, pico_path]
                    )
        except Exception as e:
            print(f"Error: {e}")

    def output_from_pico(self, file_dir):
        """
        Transfer files from Pico to computer.

        Args:
            file_dir (str): The directory path on Pico.
        """
        try:
            subprocess.run(["ampy", "--port", "/dev/ttyACM0", "get", file_dir, "."])
        except Exception as e:
            print(f"Error: {e}")

    def dir_find(self, file_dir):
        """
        Find directory or file on Pico and transfer files to C:\\pico_search.

        Args:
            file_dir (str): The directory or file to search for on Pico.
        """
        try:
            # Check if pico_search folder exists, if not, create it
            if not os.path.exists("C:/pico_search"):
                os.makedirs("C:/pico_search")

            # Search for file_dir on Pico and transfer files to C:\pico_search
            subprocess.run(
                ["ampy", "--port", "/dev/ttyACM0", "get", file_dir, "C:/pico_search"]
            )
        except Exception as e:
            print(f"Error: {e}")


# Testing Code
if __name__ == "__main__":
    # Instantiate PicoBridge
    pico_bridge = PicoBridge()
    pico_bridge.com_open()
    print(pico_bridge.com_addr)
    pico_bridge.com_close()

    # 將你想執行的命令作為列表元素
    commands = [
        "mpy-cross pico_pack/main_out.py",  # 將 example.py 轉換為 .mpy
        f"ampy --port COM14 put /main_out.mpy",  # 將 example.mpy 上傳到 Pico
        # 更多命令...
    ]

    # 執行命令
    pico_bridge.execute_commands(commands)

    # Test make_dir
    pico_bridge.make_dir("test_dir")

    # Test del_dir
    pico_bridge.del_dir("test_dir")

    # Test input_to_pico
    pico_bridge.input_to_pico("test_files")

    # Test output_from_pico
    pico_bridge.output_from_pico("/")

    # Test dir_find
    pico_bridge.dir_find("example_dir")
