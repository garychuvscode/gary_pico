import os
import pandas as pd
import requests
from io import StringIO

def version_select(version, csv_url, file_dir):
    """
    根據提供的版本號從 CSV 檔案中選擇相應的檔案連結並建立字典。
    
    參數:
    version (str): 要選擇的檔案版本，如 "V1.0"。
    csv_url (str): CSV 檔案的 URL 連結。
    file_dir (str): 指定的目錄路徑，用於存儲下載的 CSV 檔案。
    
    返回:
    dict: 字典，其索引為 file_name，值為該版本對應的檔案連結。
    """
    try:
        # 從 URL 下載 CSV 檔案內容
        response = requests.get(csv_url)
        # csv_content = response.content.decode('utf-8')
        csv_content = response.content
        
        # 將 CSV 檔案內容轉換為 DataFrame
        df = pd.read_csv(StringIO(csv_content))
        
        # 檢查提供的版本是否存在於 DataFrame 中
        if version not in df.columns:
            raise ValueError(f"Version {version} not found in CSV file.")
        
        # 建立字典：file_name 為鍵，指定版本的檔案連結為值
        version_dict = df.set_index('file_name')[version].dropna().to_dict()
        
        # 將下載的 CSV 檔案寫入指定位置
        file_path = os.path.join(file_dir, "file_list_free.csv")
        with open(file_path, 'w') as file:
            file.write(csv_content)
        
        return version_dict, file_path  # 返回 version_dict 和下載的 CSV 檔案路徑
    except Exception as e:
        print(f'Error: {e}')

# Testing the function
if __name__ == "__main__":
    # 將測試程式包成一個物件來呈現
    class TestVersionSelect:
        def __init__(self, version, csv_url, file_dir):
            self.version = version
            self.csv_url = csv_url
            self.file_dir = file_dir
            self.result = None  # 初始化 result 為 None
            self.csv_file_path = None  # 初始化 csv_file_path 為 None
            
        def test(self):
            self.result, self.csv_file_path = version_select(self.version, self.csv_url, self.file_dir)  # 將 result 和 csv_file_path 存為 self.result 和 self.csv_file_path
            print(f"Links for version {self.version}:", self.result)
    
        def cleanup(self):
            # 在完成動作後刪除下載的 CSV 檔案
            try:
                os.remove(self.csv_file_path)
                print(f"CSV file {self.csv_file_path} deleted successfully!")
            except Exception as e:
                print(f'Error: {e}')
    
    # 測試連結
    csv_url = "https://drive.google.com/file/d/1r21Myem2Ag6_dP-ToRL3jnLJ7tLcHcDQ/view?usp=drive_link"
    file_dir = "C:/g_tmp_pico/csv/"  # 請將此路徑更換為您想要存儲 CSV 檔案的目錄路徑
    
    test_obj = TestVersionSelect("V1.0", csv_url, file_dir)
    test_obj.test()
    
    # 完成動作後刪除下載的 CSV 檔案
    test_obj.cleanup()
