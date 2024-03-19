from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def list_files_in_folder(folder_name, credentials_path):
    # 建立憑證物件
    creds = Credentials.from_authorized_user_file(credentials_path)

    # 如果憑證過期，則更新憑證
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    # 建立 Google Drive API 的服務物件
    service = build("drive", "v3", credentials=creds)

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


# 範例使用方式
folder_name = "Your Folder Name"
credentials_path = "C:/py_gary/py_pico/pico-firmware-dfb0e022cc1e.json"
files_in_folder = list_files_in_folder(folder_name, credentials_path)
print("Files in folder:")
for name, file_id in files_in_folder.items():
    print(f"{name}: {file_id}")
