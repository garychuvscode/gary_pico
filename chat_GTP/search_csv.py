import csv

'''
功能描述：
- 讀取CSV文件
- 在CSV文件的每一行中尋找包含特定前綴("abc_")的元素
- 將這些元素收集到一個列表中

參數：
- file_path: CSV文件的路徑
- prefix: 我們要尋找的元素的前綴，在這個例子中為"abc_"

返回值：
- 包含所有找到的符合條件元素的列表
'''

def find_elements_with_prefix(file_path, prefix="Ver_"):
    try:
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

# 測試程式
if __name__ == "__main__":
    file_path = 'C:/g_temp_pico/file_list_free.csv'  # 請將這裡替換為您的CSV文件路徑
    found_elements = find_elements_with_prefix(file_path)
    print(found_elements)  # 輸出找到的元素
