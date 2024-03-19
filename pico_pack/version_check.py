import pandas as pd

def version_select(version):
    """
    根據提供的版本號從 CSV 檔案中選擇相應的檔案連結並建立字典。
    
    參數:
    version (str): 要選擇的檔案版本，如 "V1.0"。
    
    返回:
    dict: 字典，其索引為 file_name，值為該版本對應的檔案連結。
    """
    
    # 讀取 CSV 檔案
    df = pd.read_csv('pico_pack/file_list_free.csv')
    
    try:
        # 檢查提供的版本是否存在於 DataFrame 中
        if version not in df.columns:
            raise ValueError(f"Version {version} not found in CSV file.")
        
        # 建立字典：file_name 為鍵，指定版本的檔案連結為值
        version_dict = df.set_index('file_name')[version].dropna().to_dict()
        
        return version_dict
    except Exception as e:
        print(f'Error: {e}')

# Testing the function
if __name__ == "__main__":
    # 將測試程式包成一個物件來呈現
    class TestVersionSelect:
        def __init__(self, version):
            self.version = version
            
        def test(self):
            result = version_select(self.version)
            print(f"Links for version {self.version}:", result)
    
    test_obj = TestVersionSelect("V1.0")
    test_obj.test()
