# fmt: off
"""
this file used to generate startup process for pure
pico just installed the UF2,

file can be downloaded without licensing process
but limited to the open source folder content

need to have device selection window and
choose different device info to build up
the firmware update process with licensing
"""

# import for excel control
from datetime import datetime

# this import is for the VBA function
import win32com.client

# # also for the jump out window, same group with win32con
import win32api
import time
import pyvisa

from bs4 import BeautifulSoup

# forfile system operation
import os

# for delete function
import shutil
import requests
# fmt: off

import pandas as pd
import csv

rm = pyvisa.ResourceManager()

class startup_pico ():

    def __init__(self):


        # file: main, main_out, ws2812 (V1.0)
        self.f_list_free = [
            "https://drive.google.com/file/d/1C3uKfNAam_jvbCEko8mAGleKwRaLTiBH/view?usp=drive_link",
            "https://drive.google.com/file/d/1Iho4UCAvmH5JCXC1XlUxdqt5aso4QvJf/view?usp=drive_link",
            "https://drive.google.com/file/d/1XacaFMCTDehv7wjFZgKxgRFxwUHD9vv-/view?usp=drive_link",
        ]
        # file: pico, yd
        self.device_info = [
            "https://drive.google.com/file/d/1t5zPDsEFmmym-AeB6Yni82hOb5dprS1i/view?usp=drive_link",
            "https://drive.google.com/file/d/1a0AbOXnOGc0sF3l0iGvAu2P167-ft3mR/view?usp=drive_link",
        ]

        self.default_temp_path = "C:/g_temp_pico"
        self.startup_link = "https://drive.google.com/file/d/1r21Myem2Ag6_dP-ToRL3jnLJ7tLcHcDQ/view?usp=drive_link"
        self.startup_name = "file_list_free.csv"

        # turn off all the print delay and turn on all the index print
        # 0 => gary test mode, 1 => on line mode
        self.grace_mode = 0

        pass

    def grace_print(self, content=""):
        '''
        print the information for engineer mode
        only print when grace_mode=0, gary test mode
        '''
        if self.grace_mode == 1 :
            pass
        else:
            print(content)

        pass

    def message_box(self, content_str, title_str, box_type=0):
        '''
        message box function
        auto_exception is for waveform capture, will bypass fully auto setting in global setting \n
        boxtype(mpaaed with return value): 0-only confirm\n
        1-confirm: 1, cancel: 2
        2-stop: 3, re-try: 4, skip: 5
        3-yes: 6, no: 7, cancel: 2
        4-yes: 6, no: 7
        '''
        content_str = str(content_str)
        title_str = str(title_str)
        msg_res = 7

        msg_res = win32api.MessageBox(0, content_str, title_str, box_type)
        # 0 to 3 is different type of message box and can sen different return value
        # detail check on the internet
        print('P.S Grace is cute! ~ ')

        return msg_res

    def pwd(self, text, delay=0.04, delay_2=0.5):
        """
        Print each character of the text with a specified delay between characters.

        Parameters:
        text (str): The text to be printed.
        delay (float): The delay (in seconds) between each character.
        """
        if self.grace_mode == 0 :
            delay = 0
            delay_2 = 0

        for char in text:
            print(char, end='', flush=True)  # end='' 表示不換行，flush=True 表示立即輸出至終端
            time.sleep(delay)  # 控制延遲

        # auto to next line
        print("")
        time.sleep(delay_2)

    def download_file_from_drive(self, file_link, destination_folder=None):
        """
        Downloads a file from Google Drive with the given file ID.

        Args:
            file_id (str): The ID of the Google Drive file.
            destination_path (str): The destination path on the local machine to save the file.

        Returns:
            None
        """
        file_name0 = str(self.get_file_name_from_link(file_link))
        # Extract file ID from the link
        file_id = file_link.split("/")[5]


        destination_path = self.default_temp_path + "/" + file_name0
        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Google Drive export link for downloading files
        # export_link = f"https://drive.google.com/uc?id={file_id}"

        # Send a GET request to the export link
        download_link = f"https://drive.google.com/uc?id={file_id}"
        response = requests.get(download_link)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the downloaded file to the destination path
            with open(destination_path, "wb") as f:
                f.write(response.content)
            self.grace_print(f"File downloaded successfully to {destination_path}")
        else:
            print("Failed to download file")

    def get_file_name_from_link(self, drive_link):
        """
        Retrieves the name of a file from a Google Drive share link.

        Args:
            drive_link (str): The Google Drive share link.

        Returns:
            str: The name of the file.
        """
        # Send a GET request to the share link
        response = requests.get(drive_link)

        # Parse the HTML content of the response
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the element containing the file name
        title_element = soup.find("title")

        # Extract and return the file name
        if title_element:
            full_file_name = title_element.text.strip()
            file_name_parts = full_file_name.split(" - ")
            if len(file_name_parts) > 1:
                file_name = file_name_parts[0]
            else:
                file_name = full_file_name
            return file_name
        else:
            return None

    def delete_folder(self, folder_path=None):
        """
        Deletes a folder and all its contents.

        Args:
            folder_path (str): The path of the folder to delete.

        Returns:
            None
        """
        if folder_path == None:
            folder_path = self.default_temp_path

        shutil.rmtree(folder_path)
        self.grace_print(f"Folder deleted: {folder_path}")


    def get_elements_from_link(self, link=None, search_term="Ver_", case_sensitive=True, exactly_same=False):
        """
        Retrieves all elements containing the specified search term from a given link.

        Args:
            link (str): The link to the webpage.
            search_term (str): The search term to look for in the elements.
            case_sensitive (bool): Whether to perform a case-sensitive search. Default is True.
            exactly_same (bool): Whether to match exactly the search term. Default is False.

        Returns:
            list: A list containing all elements found in the webpage containing the search term.
        """
        if link == None:
            link = self.startup_link

        # important: from view link to donwload link


        # Send a GET request to the link
        response = requests.get(link)
        self.grace_print(response.content)

        # Parse the HTML content of the response
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all elements containing the specified search term
        if case_sensitive:
            if exactly_same:
                elements = soup.find_all(lambda tag: tag.name == "a" and tag.get_text() == search_term)
            else:
                elements = soup.find_all(lambda tag: tag.name == "a" and search_term in tag.get_text())
        else:
            search_term_lower = search_term.lower()
            if exactly_same:
                elements = soup.find_all(lambda tag: tag.name == "a" and tag.get_text().lower() == search_term_lower)
            else:
                elements = soup.find_all(lambda tag: tag.name == "a" and search_term_lower in tag.get_text().lower())

        # Extract the text from each element
        elements_list = [element.get_text().strip() for element in elements]

        return elements_list

    def find_elements_with_prefix(self, file_path=None, prefix="Ver_"):
        try:
            if file_path == None:
                file_path = f"{self.default_temp_path}/{self.startup_name}"
            elements_with_prefix = []  # 用於存儲找到的符合條件的元素

            with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:  # 遍歷CSV的每一行
                    for element in row:  # 遍歷行中的每個元素
                        if element.startswith(prefix):  # 檢查元素是否以指定的前綴開頭
                            elements_with_prefix.append(element)  # 將符合條件的元素添加到列表中

            return elements_with_prefix
        except Exception as e:
            print(f'Error: {e}')
            return []  # 遇到錯誤時返回空列表

    def version_select(self, version="Ver_1.0"):
        """
        根據提供的版本號從 CSV 檔案中選擇相應的檔案連結並建立字典。

        參數:
        version (str): 要選擇的檔案版本，如 "Ver_1.0"。

        返回:
        dict: 字典，其索引為 file_name，值為該版本對應的檔案連結。
        """

        # 讀取 CSV 檔案
        df = pd.read_csv('C:/g_temp_pico/file_list_free.csv')

        try:
            # 檢查提供的版本是否存在於 DataFrame 中
            if version not in df.columns:
                raise ValueError(f"Version {version} not found in CSV file.")

            # 建立字典：file_name 為鍵，指定版本的檔案連結為值
            version_dict = df.set_index('file_name')[version].dropna().to_dict()

            return version_dict
        except Exception as e:
            print(f'Error: {e}')
            version_dict = {}
            return version_dict


    def startup_loop(self):
        '''
        process of startup
        '''
        # self.pwd(f"Welcome to Gary's Pico tool, initialization going to start")
        # self.pwd(f"We hope to help engineers being more efficient on work")
        # self.pwd(f"And being closer to work life balance")
        # self.pwd(f"For questions and issue, please contact: gary061508@gmail.com")
        # self.pwd(f"Thanks and enjoy, by Gary Chu")
        # self.pwd(f"\nPlease make sure board is plugged in and COM number is known")

        # while 1 :
        #     # device selection
        #     self.pwd(f"What kind of board your what to use now? input: 'pico' for original or 'yd' for YD-2040")
        #     tpye_sel = input()
        #     if tpye_sel == "pico":
        #         # this is original pico
        #         device_file = 'device_info_pico.py'

        #         pass
        #     elif tpye_sel == "yd":
        #         # this is YD2040
        #         device_file = 'device_info_yd.py'

        #         pass
        #     else:
        #         self.pwd(f"GG, input incorrect, please try again~ @@")

        #     if tpye_sel == "pico" or tpye_sel == "yd" :
        #         self.pwd(f"is '{tpye_sel}' correct? 'y' for next step and 'n' for re-input ")
        #         temp_ans = input()
        #         if temp_ans == 'y':
        #             break


        #     # end of while
        #     pass
        # self.pwd(f"'{tpye_sel}' is choose by user")


        # while 1 :
        #     # COM number selection

        #     self.pwd(f"Please enter to correct COM number for plugged board")
        #     com_num = input()

        #     try:
        #         com_test = rm.open_resource(f"COM{com_num}")

        #         # close if success
        #         self.pwd(f"COM{com_num}, connteced ok, now update firmware")
        #         # close and release COM port
        #         com_test.close()

        #         # break the loop after COM port number input correct
        #         break

        #     except Exception as e:

        #         self.pwd(f"GG, input incorrect, please try again, error message:")
        #         print(e)

        #     # end while
        #     pass

        # check available version and list for user to select:


        # 240319: the csv in google can't be read, error
        # ver_info = self.get_elements_from_link()
        self.download_file_from_drive(self.startup_link)
        ver_info = self.find_elements_with_prefix()

        # prevent the file been seen during user input
        self.delete_folder(self.default_temp_path)

        self.pwd(f"The version we have on the server, select the version needed:")
        print(ver_info)
        print("Input must be the same!")
        # download file from google
        ver_sel = input("Please choose version: ")

        # there may hacve version check function already
        # for ver_inf in ver_info :
        #     if ver_inf == ver_sel :
        #         # find the correct version, knowing the link


        # download again after choosing version is finished
        self.download_file_from_drive(self.startup_link)
        # choose related link for down load file
        file_list = self.version_select(version=ver_sel)

        for file_name, link in file_list.items():  # 遍歷字典中的每個鍵值對
            if file_name != 'comments':  # 排除非文件鏈接的條目
                self.download_file_from_drive(link)  # 使用文件下載函數下載文件

        # download finished here


        self.pwd(f"")
        self.pwd(f"")
        self.pwd(f"")
        self.pwd(f"")
        self.pwd(f"")




        # delete all the file download when process done
        self.delete_folder()
        pass



world_of_pico = startup_pico()
world_of_pico.startup_loop()


# Testing code
if __name__ == "__main__":


    pass
