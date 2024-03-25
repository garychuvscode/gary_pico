import xlwings as xw

class version_file_update:
    def __init__(self):
        self.app = xw.App(visible=True)
        self.column_index = []
        self.row_index = []

    def open_file(self, file_path):
        self.wb = self.app.books.open(file_path)
        self.sheet = self.wb.sheets[0]  # 打開第一個工作表
        self.column_index = [self.sheet.range((1, col)).value for col in range(1, self.sheet.used_range.last_cell.column + 1)]
        self.row_index = [self.sheet.range((row, 1)).value for row in range(1, self.sheet.used_range.last_cell.row + 1)]

    def version_select(self, version_name):
        if version_name in self.column_index:
            col_num = self.column_index.index(version_name) + 1
            content_dict = {self.sheet.range((row, 1)).value: self.sheet.range((row, col_num)).value for row in range(2, len(self.row_index) + 1)}
            return content_dict
        else:
            return {}

    def add_version(self, version_name, version_comment, file_list):
        if version_name not in self.column_index:
            new_col_num = len(self.column_index) + 1
            self.sheet.range((1, new_col_num)).value = version_name
            self.column_index.append(version_name)
            
            # 搜尋 "comments" 行的行號
            comments_row = None
            if "comments" in self.row_index:
                comments_row = self.row_index.index("comments") + 1  # +1 因為Excel行是從1開始的，而不是從0開始
            else:
                # 如果沒有找到 "comments"，則假設它在第二行
                comments_row = 2

            # 在 "comments" 行的對應列中添加註釋
            self.sheet.range((comments_row, new_col_num)).value = version_comment

        # 更新檔案列表到新版本列
        for file_name, content in file_list.items():
            if file_name in self.row_index:
                row_num = self.row_index.index(file_name) + 1  # Excel行從1開始
            else:
                # 如果檔案名稱不在現有行中，則添加到最後
                row_num = len(self.row_index) + 1
                self.sheet.range((row_num, 1)).value = file_name
                self.row_index.append(file_name)

            # 在對應行列中添加檔案內容
            self.sheet.range((row_num, new_col_num)).value = content

    def delete_version(self, version_name):
        if version_name in self.column_index:
            col_num = self.column_index.index(version_name) + 1
            self.sheet.api.Columns(col_num).Delete()
            self.column_index.remove(version_name)

    def save_close(self, file_path=None):
        if file_path:
            self.wb.save(file_path)
        self.wb.close()
        self.app.quit()


# Testing code
if __name__ == "__main__":



    # 假定Excel文件名為 'test.xlsx'，位於當前目錄
    file_path = "C:/py_google/file_list_free.xlsx"

    # 初始化 version_file_update 對象
    vf_update = version_file_update()

    # 打開 Excel 文件並加載索引
    vf_update.open_file(file_path)

    # 假定要選擇的版本名為 'Ver_1.0'
    version_to_select = 'Ver_1.0'
    selected_version_content = vf_update.version_select(version_to_select)
    print(f"內容於 {version_to_select} 版本中：")
    for row_index, content in selected_version_content.items():
        print(f"{row_index}: {content}")

    # 添加一個新版本
    new_version_name = 'Ver_1.3'
    new_version_comment = 'comments'
    new_file_list = {
        'main.py': '內容1',
        'file_2': '內容2',
        'new_file': '新檔案的內容'
    }
    vf_update.add_version(new_version_name, new_version_comment, new_file_list)

    # 刪除一個版本
    version_to_delete = 'Ver_1.1'
    vf_update.delete_version(version_to_delete)

    # 儲存並關閉 Excel 文件
    vf_update.save_close()

    print("測試完成，請檢查 Excel 文件以確認變更。")