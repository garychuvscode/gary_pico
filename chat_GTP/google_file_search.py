import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth.transport.requests
import google.oauth2.credentials

class GoogleDriveCredentials:
    """
    用於存儲和管理 Google Drive API 認證的類別。
    """
    def __init__(self, client_id, client_secret, refresh_token, access_token, token_uri='https://oauth2.googleapis.com/token'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.token_uri = token_uri
        self.access_token = access_token

    def create_credentials(self):
        """
        創建一個 Google OAuth2 認證對象。
        """
        return Credentials(
            None,
            refresh_token=self.refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_uri=self.token_uri
        )

def list_files_in_folder(folder_name, creds):
    """
    列出指定 Google Drive 資料夾中的所有檔案。
    folder_name: 資料夾名稱
    creds: GoogleDriveCredentials 的實例
    """
    try:
        # 使用 GoogleDriveCredentials 類別的實例來獲取認證
        credentials = creds.create_credentials()

        # 如果憑證過期，則更新憑證
        print(f'exp:{credentials.expired}; refresh:{credentials.refresh_token}')
        
        # 建立 Google Drive API 的服務物件
        service = build("drive", "v3", credentials=credentials)

        # 查詢資料夾 ID
        folder_id = None
        page_token = None
        while True:
            response = (
                service.files()
                .list(
                    q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'",
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
        page_token = None
        while True:
            response = (
                service.files()
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

        return file_list

    except Exception as e:
        print(f"Error: {e}")
        return {}

# 測試代碼
if __name__ == "__main__":
    # 填入你的認證信息
    client_id = ""
    client_secret = ""
    refresh_token = ""
    access_token = ""
    

    # 創建一個 Google OAuth 2.0 憑據實例
    creds = google.oauth2.credentials.Credentials(
        token=access_token,
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        scopes = "https://www.googleapis.com/auth/drive"
    )

    # 建立一個 Request 物件
    request = google.auth.transport.requests.Request()

    # 使用 Google OAuth 2.0 憑據實例來獲取認證
    credentials = creds.refresh_token(request)

    # 使用認證後的憑據來建立 Google Drive API 服務
    service = build('drive', 'v3', credentials=credentials)


    # 執行檔案列出功能
    folder_name = "V1.0"
    files_in_folder = list_files_in_folder(folder_name, creds)
    print("Files in folder:")
    for name, file_id in files_in_folder.items():
        print(f"{name}: {file_id}")
