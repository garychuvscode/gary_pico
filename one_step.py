# fmt: off
"""
this file used to summary the steps need to finished firmware
upload to internet from the original y code of pico

include below steps:
1. enter the version information and comments here
(also choose to add new or delete old)
2. make file become mpy, and move to related folder
3. after the upload finished, check on google drive API for file id
4. based on the input version_name and comments => create
the version _folder and file_name to the version_list.xlsx

"""

import subprocess
import os
import shutil

from google_drive_obj import GoogleDrive_Ctrl_obj
from version_file_obj import version_file_update
import credential_helper_obj as cre  # 假設有一個用於加載認證的幫助函數
import prograss_bar as pg

import time

# 設置Google Drive API的認證
cred_ctrl = cre.crediential_helper()
cred_dict = cred_ctrl.load_credentials()
google_drive_ctrl = GoogleDrive_Ctrl_obj(cred_dict=cred_dict)

# 設置版本名和文件列表
# version_name = "V1.0"  # 版本名稱，來自 one_step.py
# file_list = ["main_out", "pio_ws2812_obj"]  # 文件列表，來自 one_step.py
# file_list.append("main")  # 添加額外的 main.py 文件

def get_file_ids_and_update(version_name, file_list, comments0= None):
    """
    獲取特定版本資料夾中每個文件的 file_id 並更新 Excel 列表。
    """
    file_ids = {}
    if comments0 == None :
        comments0 = version_name

    # 獲取每個文件的 file_id
    for file_name in file_list:
        file_id = google_drive_ctrl.get_file_id_by_name(f"{file_name}.mpy", parent_folder_id=google_drive_ctrl.get_folder_id_by_name(version_name))
        if file_id:
            file_ids[f"{file_name}.mpy"] = file_id
        else:
            print(f"file not found: {file_name}.mpy")

    # 更新 Excel 列表
    if file_ids:
        version_updater = version_file_update()
        version_updater.auto_update(file_ids, version_name, comments0)

    return file_ids

# ===============================

# '''功能說明：此代碼片段整合了檔案轉換與檔案移動的過程，用於將指定的 Python 檔案列表轉換為 .mpy 格式，並將轉換後的檔案移動到指定的雲端硬碟路徑。
# 變數說明：
# - mode: 操作模式
# - version_name: 版本名稱，用於建立目的資料夾
# - file_list: 包含要轉換的 Python 檔案名稱的列表
# '''

def convert_and_move_files(file_list, version_name, type_folder):
    """
    轉換指定列表中的 Python 檔案為 .mpy 格式，並將轉換後的檔案移動到指定的雲端硬碟路徑。

    Parameters:
    - file_list (list): 要轉換的 Python 檔案名稱列表
    - version_name (str): 雲端硬碟中版本資料夾的名稱
    - type_folder (str): 分類資料夾的名稱
    """
    try:
        # 目的資料夾的基本路徑
        base_file_dist = f"G:\\我的雲端硬碟\\pico_release\\{type_folder}\\{version_name}"

        for file_name in file_list:
            # 執行檔案轉換命令
            subprocess.run(f"mpy-cross {file_name}.py", shell=True, check=True)

            # 計算目的地檔案路徑
            file_dist = os.path.join(base_file_dist, f"{file_name}.mpy")

            # 確保目的資料夾存在
            os.makedirs(os.path.dirname(file_dist), exist_ok=True)

            # 移動 .mpy 檔案到目的地
            shutil.move(f"{file_name}.mpy", file_dist)

            print(f"{file_name}.mpy has been converted and moved successfully.")

        # 將 main.py 複製到目的資料夾
        shutil.copy("main.py", base_file_dist)
        print('main.py copy done')

    except Exception as e:
        print(f"Error occurred: {e}")

# ===========================================

def delete_version_by_name(version_name):
    """
    根据提供的 version_name 删除指定的版本。
    """
    try:
        # 初始化 version_file_update 类的实例
        version_updater = version_file_update()

        # 删除指定的版本
        version_updater.auto_delete(version_name0=version_name)

        print(f" {version_name} has been deleted ")
    except Exception as e:
        print(f"error delete the version {e}")

def delete_local_folder(type_folder, version_name):
    """
    從本機路徑刪除指定的資料夾及其所有內容。

    Parameters:
    - type_folder (str): 分類資料夾的名稱
    - version_name (str): 版本資料夾的名稱
    """
    base_file_dist = f"G:\\我的雲端硬碟\\pico_release\\{type_folder}\\{version_name}"
    try:
        # 檢查目錄是否存在
        if os.path.exists(base_file_dist) and os.path.isdir(base_file_dist):
            shutil.rmtree(base_file_dist)
            print(f"The folder '{base_file_dist}' has been deleted successfully.")
        else:
            print(f"The folder '{base_file_dist}' does not exist.")
    except Exception as e:
        print(f"An error occurred while trying to delete the folder '{base_file_dist}': {e}")

# 測試代碼
if __name__ == "__main__":

    # input the control information, choose add, del, list
    mode = "add"
    # input the version_name (folder name)
    version_name = "V1.1"
    # type selection for free or full
    type_sel = "full"
    # input the list of file_name for this version (main.py auto include)
    file_list = [
        "main_out",
        "pio_ws2812_obj",
    ]
    comments = "this is version comments1 "
    time_wait = 10

    if type_sel == "free":
        folder_name="free_version"
    else:
        folder_name="full_version"

    if mode == "add":
        print(f"now is in {mode} mode ~ , type-{type_sel}, version-{version_name}, comment-{comments} ")
        print(f"and the file list is: {file_list}")
        x = input("are you sure? y or n ")
        if x == "y":

            file_list_2 = convert_and_move_files(file_list, version_name, folder_name)

            # for i in range(100 + 1):
            #     time.sleep(time_wait/100)  # 模擬一些工作
            #     pg.prog_bar_2(i, 100, prefix='Upload file:', suffix='Complete', length=50, fill_str='New ver done', fill_char='>', adjust='left')

            file_ids = get_file_ids_and_update(version_name, file_list, comments)
            print("updated ids", file_ids)

    elif mode == "list" :
        print(f"now is in {mode} mode ~ type-{type_sel}")
        files_in_folder = google_drive_ctrl.list_files_in_folder(folder_name, depth_scan=1)

        pass

    elif mode == "del":
        print(f"now is in {mode} mode ~ , type-{type_sel}, version-{version_name}")
        x = input("are you sure? y or n ")
        if x == "y":
            delete_version_by_name(version_name)
            delete_local_folder(folder_name, version_name)

    else:
        print(f"input: {mode} wrong, with version: {version_name}")
        print("please check and run again")
