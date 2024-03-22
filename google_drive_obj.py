import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


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
        account = "nova781", 
        cred_dict=None
    ):
        if cred_dict == None: 
            # load from direct iput
            self.client_id = client_id
            self.client_secret = client_secret
            self.refresh_token = refresh_token
            
        else : 
            # or load from loder output dictionary
            self.client_id = cred_dict["client_id"]
            self.client_secret = cred_dict["client_secret"]
            self.refresh_token = cred_dict["refresh_token"]

        self.token_uri = token_uri
        self.access_token = access_token

        self.default_crediential_path = f"C:/py_google/{account}.txt"

        # this is the service object for other operation
        self.service = self.open_service()

    def open_service(self): 
        """
        open the service channel for google drive
        """
        service = "sevice not assigned yet"

        try: 
            # create credential object
            credentials = self.create_credentials()
            # update everytime open the object
            credentials.refresh(Request())

            # 建立 Google Drive API 的服務物件
            service = build("drive", "v3", credentials=credentials)

        except Exception as e : 
            print(f'open service fail, check on google cloud for status')
            print(f'if the refresh_token need to be reset (usually 1 year)')

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


    def list_files_in_folder(self, folder_name0):
        """
        列出指定 Google Drive 資料夾中的所有檔案。
        folder_name: 資料夾名稱
        """
        try:
            
            # 查詢資料夾 ID
            folder_id = None
            page_token = None
            while True:
                response = (
                    self.service.files()
                    .list(
                        q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )
                for file in response.get("files", []):
                    if file.get("name") == folder_name0:
                        folder_id = file.get("id")
                        break
                page_token = response.get("nextPageToken")
                if page_token is None:
                    break

            # 如果找不到資料夾，則回傳空字典
            if folder_id is None:
                print(f"Cannot find folder with name '{folder_name0}'")
                return {}

            # 列出資料夾中的檔案
            file_list = {}
            page_token = None
            while True:
                response = (
                    self.service.files()
                    .list(
                        q=f"'{folder_id}' in parents",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )
                for file in response.get("files", []):
                    file_list[file.get("name")] = file.get("id")
                page_token = response.get("nextPageToken")
                if page_token is None:
                    break
            
            # print before return dictionary
            print(f"Files in folder '{folder_name0}' :")
            for name, file_id in file_list.items():
                print(f"{name}: {file_id}")

            return file_list

        except Exception as e:
            print(f"Error: {e}")
            return {}


# 測試代碼
if __name__ == "__main__":

    import credential_helper_obj as cre

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
    google_ctrl = GoogleDrive_Ctrl_obj(
        cred_dict=cred_dict0
    )

    # 執行檔案列出功能
    folder_name = "V1.1"

    files_in_folder = google_ctrl.list_files_in_folder(folder_name)
    
