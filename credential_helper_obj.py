import ast

credentials = dict()

class crediential_helper ():

    def __init__(self, file_name0='nova781.txt'):

        # self.file_path0 = f"C:/py_google/{file_name0}"
        self.file_path0 = f"G:/我的雲端硬碟/py_google/{file_name0}"

    def load_credentials(self, file_path=None):
        """
        從指定的本機路徑加載認證信息。

        Args:
            file_path (str): 包含認證字典的文本文件的路徑。

        Returns:
            dict: 包含認證信息的字典。
        """
        if file_path == None:
            file_path = self.file_path0
        try:
            # 打開文件並讀取內容
            with open(file_path, 'r') as file:
                content = file.read()
                
                # 將字符串內容轉換為字典
                credentials_dict = ast.literal_eval(content)
                
                # 確保所有必需的鍵都在字典中
                # required_keys = ['client_id', 'client_secret', 'refresh_token', 'access_token']
                required_keys = ['client_id', 'client_secret', 'refresh_token',]
                if not all(key in credentials_dict for key in required_keys):
                    raise ValueError("Credentials file is missing required keys.")
                
                print("Credentials successfully load from file.")
                return credentials_dict

        except Exception as e:
            print(f"Error loading credentials: {e}")
            return {}


    def save_credentials_to_file(self, credentials_dict, file_path=None):
        """
        將認證信息保存到指定的文本文件中。

        Args:
            credentials_dict (dict): 包含認證信息的字典。
            file_path (str): 目標文本文件的絕對路徑。

        Returns:
            bool: 操作是否成功。
        """
        if file_path == None:
            file_path = self.file_path0
        try:
            # 確保傳入的 credentials_dict 是字典並且包含所有必要的鍵
            # required_keys = ['client_id', 'client_secret', 'refresh_token', 'access_token']
            required_keys = ['client_id', 'client_secret', 'refresh_token',]
            if not isinstance(credentials_dict, dict) or not all(key in credentials_dict for key in required_keys):
                raise ValueError("Invalid credentials format or missing keys.")
            
            # 打開指定的文件並寫入認證信息
            with open(file_path, 'w') as file:
                # 將字典轉化為字符串並寫入文件
                file.write(str(credentials_dict))

            print("Credentials successfully saved to file.")
            return True

        except Exception as e:
            print(f"Error saving credentials to file: {e}")
            return False



# Testing code
if __name__ == "__main__":

    cred_access = crediential_helper(file_name0='cre_testing.txt')

    credentials_path = "G:/我的雲端硬碟/py_google/cre_testing.txt"
    credentials = cred_access.load_credentials(credentials_path)

    if credentials:
        client_id = credentials['client_id']
        client_secret = credentials['client_secret']
        refresh_token = credentials['refresh_token']
        # access_token = credentials['access_token']
        # 接下來，你可以使用這些認證信息來創建 GoogleDriveCredentials 實例或進行其他操作

    # ==================================

    credentials = {
        "client_id": f"{client_id}_1",
        "client_secret": f"{client_secret}_1",
        "refresh_token": f"{refresh_token}_1",
        # "access_token": f"{access_token}_1"
    }

    file_path = "G:/我的雲端硬碟/py_google/cre_testing.txt"
    success = cred_access.save_credentials_to_file(credentials, file_path)

    # if success:
    #     print("Credentials successfully saved to file.")
    # else:
    #     print("Failed to save credentials to file.")
