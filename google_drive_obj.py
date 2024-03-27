import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload  # Add this import statement

import pandas as pd
import xlwings as xw

# fmt: off

class GoogleDrive_Ctrl_obj:
    """
    this is for google drive related operation
    class only for internal used only, since there are credential needed
    for specific account
    """

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        refresh_token=None,
        access_token=None,
        token_uri="https://oauth2.googleapis.com/token",
        account="nova781",
        cred_dict=None,
    ):
        if cred_dict == None:
            # load from direct iput
            self.client_id = client_id
            self.client_secret = client_secret
            self.refresh_token = refresh_token

        else:
            # or load from loder output dictionary
            self.client_id = cred_dict["client_id"]
            self.client_secret = cred_dict["client_secret"]
            self.refresh_token = cred_dict["refresh_token"]

        self.token_uri = token_uri
        self.access_token = access_token

        self.default_crediential_path = f"C:/py_google/{account}.txt"

        # this is the service object for other operation
        self.credentials = self.create_credentials()
        self.service = self.open_service()

        self.default_csv_path = f"C:/py_google/"

    def open_service(self):
        """
        open the service channel for google drive
        """
        service = "sevice not assigned yet"

        try:
            # update everytime open the object
            self.credentials.refresh(Request())

            # 建立 Google Drive API 的服務物件
            service = build("drive", "v3", credentials=self.credentials)

        except Exception as e:
            print(f"open service fail, check on google cloud for status")
            print(f"if the refresh_token need to be reset (usually 1 year)")

        return service

    def create_credentials(self):
        """
        創建一個 Google OAuth2 認證對象。
        """
        return Credentials(
            token=self.access_token,
            refresh_token=self.refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_uri=self.token_uri,
        )

    def update_file_list(self, file_name, drive_folder_name):
        """
        update the file list to excel file, then pass to pandas to
        transfer to csv
        """
        file_path = f"{self.default_csv_path}{file_name}.xlsx"
        wb_list = xw.Book(file_path)



    # def list_files_in_folder(self, folder_name0):
    #     """
    #     列出指定 Google Drive 資料夾中的所有檔案。
    #     folder_name: 資料夾名稱
    #     """
    #     try:

    #         # 查詢資料夾 ID
    #         folder_id = None
    #         page_token = None
    #         while True:
    #             response = (
    #                 self.service.files()
    #                 .list(
    #                     q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'",
    #                     spaces="drive",
    #                     fields="nextPageToken, files(id, name)",
    #                     pageToken=page_token,
    #                 )
    #                 .execute()
    #             )
    #             for file in response.get("files", []):
    #                 if file.get("name") == folder_name0:
    #                     folder_id = file.get("id")
    #                     break
    #             page_token = response.get("nextPageToken")
    #             if page_token is None:
    #                 break

    #         # 如果找不到資料夾，則回傳空字典
    #         if folder_id is None:
    #             print(f"Cannot find folder with name '{folder_name0}'")
    #             return {}

    #         # 列出資料夾中的檔案
    #         file_list = {}
    #         page_token = None
    #         while True:
    #             response = (
    #                 self.service.files()
    #                 .list(
    #                     q=f"'{folder_id}' in parents",
    #                     spaces="drive",
    #                     fields="nextPageToken, files(id, name)",
    #                     pageToken=page_token,
    #                 )
    #                 .execute()
    #             )
    #             for file in response.get("files", []):
    #                 file_list[file.get("name")] = file.get("id")
    #             page_token = response.get("nextPageToken")
    #             if page_token is None:
    #                 break

    #         # print before return dictionary
    #         print(f"Files in folder '{folder_name0}' :")
    #         for name, file_id in file_list.items():
    #             print(f"{name}: {file_id}")

    #         return file_list

    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return {}

    def check_and_refresh_credentials(self):
        """
        檢查並刷新過期的認證。
        """
        if self.credentials.expired:
            print("Credentials have expired, refreshing...")
            self.credentials.refresh(Request())
            print("Credentials refreshed.")
        else:
            print("Credentials are still valid.")

    # ==============================

    def get_folder_id_by_name(self, folder_name, parent_folder_id=None):
        """
        根據資料夾名稱獲取資料夾的 ID。
        Args:
            folder_name (str): 資料夾的名稱。
        Returns:
            str: 資料夾的 ID，如果未找到則返回 None。
        """
        query = (
            f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
        )
        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"

        response = self.service.files().list(q=query, fields="files(id)").execute()
        folders = response.get("files", [])
        
        if folders:
            print(f'get folder: {folder_name} with id {folders[0].get("id")} \n from parent {parent_folder_id}')
            return folders[0].get("id")
        return None

    def get_file_id_by_name(self, file_name, parent_folder_id=None):
        """
        根據檔案名稱獲取檔案的 ID。
        Args:
            file_name (str): 檔案的名稱。
            parent_folder_id (str): 父資料夾的 ID，如果指定，則只在該資料夾內搜索。

        Returns:
            str: 檔案的 ID，如果未找到則返回 None。
        """
        query = f"name='{file_name}'"
        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"
        response = self.service.files().list(q=query, fields="files(id)").execute()
        files = response.get("files", [])
        

        if files:
            print(f'get file: {file_name} with id {files[0].get("id")} \n from parent {parent_folder_id}')
            return files[0].get("id")
        return None

    def create_folder(self, name, parent_folder_name=None):
        """
        在 Google Drive 中創建一個新資料夾，如果資料夾已存在，則返回現有資料夾的 ID。

        Args:
            name (str): 新資料夾的名稱。
            parent_folder_name (str): 父資料夾的名稱。

        Returns:
            str: 資料夾的 ID。
        """
        # 檢查是否已存在同名資料夾
        existing_folder_id = self.get_folder_id_by_name(name)
        if existing_folder_id:
            print(f"Folder '{name}' already exists. Using the existing folder.")
            return existing_folder_id

        # 檢查是否指定了父資料夾名稱，並獲取父資料夾 ID
        parent_id = None
        if parent_folder_name:
            parent_id = self.get_folder_id_by_name(parent_folder_name)
            if parent_id is None:
                print(
                    f"Parent folder '{parent_folder_name}' not found. Creating '{name}' in the root."
                )

        # 創建新資料夾
        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id] if parent_id else [],
        }
        folder = self.service.files().create(body=file_metadata, fields="id").execute()
        print(f"Folder '{name}' created with ID: {folder.get('id')}")
        return folder.get("id")

    def list_files_in_folder(self, folder_name, depth_scan=3):
        """
        列出指定 Google Drive 資料夾中的所有檔案。
        folder_name (str): 資料夾名稱。
        depth_scan (int): 掃描的最大深度。0 表示掃描所有層，正整數表示要掃描的層數。默認為 3。
        """
        # clear trash before search, prevent to see deleted version with same name
        self.empty_trash()

        try:
            # 查詢資料夾 ID
            folder_id = None
            page_token = None
            while True:
                """
                query (q): content and note: 
                mimeType='application/vnd.google-apps.folder'：查找的是文件夹。
                name='{folder_name}'：文件夹的名称必须匹配 folder_name 变量的值。
                trashed = false：文件夹不在回收站中。
                """
                response = (
                    self.service.files()
                    .list(
                        q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed = false",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )
                for file in response.get("files", []):
                    if file.get("name") == folder_name:
                        folder_id = file.get("id")
                        break
                page_token = response.get("nextPageToken")
                if page_token is None:
                    break

            # 如果找不到資料夾，則回傳空字典
            if folder_id is None:
                print(f"Cannot find folder with name '{folder_name}'")
                return {}

            # 列出資料夾中的檔案
            file_list = {}

            def list_files_recursive(folder_id, current_depth=1, indent_level=0):
                nonlocal file_list
                if depth_scan > 0 and current_depth > depth_scan:
                    return
                page_token = None
                while True:
                    response = (
                        self.service.files()
                        .list(
                            q=f"'{folder_id}' in parents",
                            spaces="drive",
                            fields="nextPageToken, files(id, name, mimeType)",
                            pageToken=page_token,
                        )
                        .execute()
                    )
                    for file in response.get("files", []):
                        indent = "\t" * indent_level
                        if file.get("mimeType") == "application/vnd.google-apps.folder":
                            print(f"{indent}folder: {file.get('name')}")
                            list_files_recursive(file.get("id"), current_depth + 1, indent_level + 1)
                        else:
                            print(f"{indent}file: {file.get('name')}")
                            file_list[file.get('name')] = file.get("id")
                    page_token = response.get("nextPageToken")
                    if page_token is None:
                        break

            list_files_recursive(folder_id)

            return file_list

        except Exception as e:
            print(f"Error: {e}")
            return {}

    def rename_file(self, old_name, new_name, parent_folder_name=None):
        """
        重命名 Google Drive 中的檔案。

        Args:
            old_name (str): 檔案的舊名稱。
            new_name (str): 檔案的新名稱。
            parent_folder_name (str): 檔案所在的父資料夾名稱。

        Returns:
            bool: 操作是否成功。
        """
        parent_id = None
        if parent_folder_name:
            parent_id = self.get_folder_id_by_name(parent_folder_name)

        file_id = self.get_file_id_by_name(old_name, parent_id)
        if not file_id:
            print(f"File '{old_name}' not found.")
            return False

        try:
            self.service.files().update(
                fileId=file_id, body={"name": new_name}
            ).execute()
            return True
        except Exception as e:
            print(f"Error renaming file: {e}")
            return False

    def empty_trash(self):
        """
        清空 Google Drive 的垃圾桶。
        """
        try:
            self.service.files().emptyTrash().execute()
            print("Trash has been emptied successfully.")
        except Exception as e:
            print(f"An error occurred while trying to empty the trash: {e}")
    
    def delete_folder_by_name(self, folder_name):
        """
        根據資料夾名稱刪除 Google Drive 上的資料夾。

        Args:
            folder_name (str): 要刪除的資料夾的名稱。
        """
        try:
            # 查找資料夾的 ID
            folder_id = self.get_folder_id_by_name(folder_name)
            if folder_id:
                # 呼叫 Google Drive API 進行刪除
                self.service.files().delete(fileId=folder_id).execute()
                print(f"Folder '{folder_name}' has been deleted successfully.")
            else:
                print(f"Folder '{folder_name}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def upload_file(self, file_path, parent_folder_name=None):
        """
        將文件上傳到指定的 Google Drive 資料夾。

        Args:
            file_path (str): 本地文件的絕對路徑。
            parent_folder_name (str): 目標資料夾的名稱。如果為 None，文件將被上傳到根目錄。

        Returns:
            str: 上傳的文件的 ID。
        """
        parent_id = None
        if parent_folder_name:
            parent_id = self.get_folder_id_by_name(parent_folder_name)
            if parent_id is None:
                print(f"Folder '{parent_folder_name}' not found. Uploading to root.")

        file_metadata = {
            "name": os.path.basename(file_path),
            "parents": [parent_id] if parent_id else [],
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        return file.get("id")

    def share_file(self, shared_item_name, role="reader", type="anyone"):
        """
        設定 Google Drive 文件或資料夾的分享權限。

        Args:
            shared_item_name (str): 文件或資料夾的名稱。
            role (str): 分享的角色（'owner', 'organizer', 'fileOrganizer', 'writer', 'commenter', 'reader'）。
            type (str): 分享的類型（'user', 'group', 'domain', 'anyone'）。

        Returns:
            str: 文件或資料夾的分享連結。
        """
        item_id = self.get_file_id_by_name(shared_item_name)
        if item_id is None:
            item_id = self.get_folder_id_by_name(shared_item_name)
            if item_id is None:
                print(f"Item '{shared_item_name}' not found.")
                return None

        self.service.permissions().create(
            fileId=item_id, body={"role": role, "type": type}, fields="id"
        ).execute()

        response = (
            self.service.files().get(fileId=item_id, fields="webViewLink").execute()
        )
        return response.get("webViewLink")


# 測試代碼
if __name__ == "__main__":

    import credential_helper_obj as cre

    # cred_ctrl = cre.crediential_helper(file_name0='gary4990')
    cred_ctrl = cre.crediential_helper()
    cred_dict0 = cred_ctrl.load_credentials()

    # 填入你的認證信息
    # client_id = (
    #     "client_id_here"
    # )
    # client_secret = "client_secret_here"
    # refresh_token = "refresh_token_here"

    # google_ctrl = GoogleDrive_Ctrl_obj(
    #     client_id, client_secret, refresh_token
    # )
    google_ctrl = GoogleDrive_Ctrl_obj(cred_dict=cred_dict0)


    test_index = 1

    if test_index == 0 :

        # 執行檔案列出功能
        folder_name = "V1.1"
        # folder_name = "pico_release"

        files_in_folder = google_ctrl.list_files_in_folder(folder_name)

        # testing for upload file
        google_ctrl.upload_file(file_path="C:/py_google/testing_note.txt")

        # 測試創建資料夾
        print("Testing folder creation...")
        folder_name = "TestFolder"
        folder_id = google_ctrl.create_folder(folder_name)
        print(f"Folder '{folder_name}' created with ID: {folder_id}")

        # 測試列出資料夾中的檔案
        folder_name = "pico_release"
        print(f"Listing files in folder '{folder_name}'...")
        files = google_ctrl.list_files_in_folder(folder_name)
        # for file in files:
        #     print(file)

        # 測試重命名檔案（請根據你的實際情況替換 'old_file_name' 和 'new_file_name'）
        old_file_name = "TestFolder"
        new_file_name = "TestFolder2"
        print(f"Renaming file '{old_file_name}' to '{new_file_name}'...")
        success = google_ctrl.rename_file(old_file_name, new_file_name)
        if success:
            print(f"File '{old_file_name}' successfully renamed to '{new_file_name}'")
        else:
            print(f"Failed to rename file '{old_file_name}'")

        # 測試設定檔案分享權限（請根據你的實際情況替換 'file_name_to_share'）
        file_name_to_share = "a142"
        print(f"Setting share permissions for file '{file_name_to_share}'...")
        share_link = google_ctrl.share_file(file_name_to_share)
        print(f"Share link for file '{file_name_to_share}': {share_link}")

        # 測試重命名檔案（請根據你的實際情況替換 'old_file_name' 和 'new_file_name'）
        old_file_name = "TestFolder2"
        new_file_name = "TestFolder"
        print(f"Renaming file '{old_file_name}' to '{new_file_name}'...")
        success = google_ctrl.rename_file(old_file_name, new_file_name)
        if success:
            print(f"File '{old_file_name}' successfully renamed to '{new_file_name}'")
        else:
            print(f"Failed to rename file '{old_file_name}'")


        pass

    elif test_index == 1 :

        csv_name = "file_list_free"  # 請替換成你的CSV檔案路徑
        drive_folder_name = "V1.2"  # 替換成你的Google Drive資料夾名稱
        # google_ctrl.update_file_list_csv(csv_name, drive_folder_name)

        pass
