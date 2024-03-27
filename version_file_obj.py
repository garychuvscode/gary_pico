import xlwings as xw

# also for the jump out window, same group with win32con
import win32api

# fmt: off
class version_file_update:
    def __init__(self):
        self.app = xw.App(visible=True)
        self.column_index = []
        self.row_index = []
        self.default_file_path = "G:/我的雲端硬碟/py_google/"
        self.default_file_name = "full_version"
        self.full_path = ""
        # same version or other issue to exit
        self.cancel = 0
    def open_file(self, file_name=None):

        if file_name == None:
            self.full_path = self.default_file_path + "list_" + self.default_file_name + ".xlsx"
            pass
        else:
            self.full_path = f"{self.default_file_path}list_{file_name}.xlsx"
            pass
        self.wb = self.app.books.open(self.full_path)
        # 240326 not to use this one, prevent app issue, not close or interrupt by others
        # self.wb = xw.Book(self.full_path)
        self.sheet = self.wb.sheets[0]  # 打開第一個工作表
        self.column_index = [
            self.sheet.range((1, col)).value
            for col in range(1, self.sheet.used_range.last_cell.column + 1)
        ]
        self.row_index = [
            self.sheet.range((row, 1)).value
            for row in range(1, self.sheet.used_range.last_cell.row + 1)
        ]

    def version_select(self, version_name):
        if version_name in self.column_index:
            col_num = self.column_index.index(version_name) + 1
            content_dict = {
                self.sheet.range((row, 1)).value: self.sheet.range((row, col_num)).value
                for row in range(2, len(self.row_index) + 1)
            }
            return content_dict
        else:
            return {}

    def add_version(self, version_name, version_comment, file_list):
        if version_name not in self.column_index:
            new_col_num = len(self.column_index) + 1
            self.sheet.range((1, new_col_num)).value = version_name
            self.column_index.append(version_name)

        else:
            # 如果版本名稱已存在，找到對應的列索引
            existing_col_num = self.column_index.index(version_name) + 1
            new_col_num = existing_col_num
            self.message_box("enter and cancel update", f"version {version_name} already exist")
            self.cancel = 1

        if self.cancel == 0 :

            # 搜尋 "comments" 行的行號
            comments_row = None
            if "comments" in self.row_index:
                comments_row = (
                    self.row_index.index("comments") + 1
                )  # +1 因為Excel行是從1開始的，而不是從0開始
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
        else:
            self.cancel = 1
            self.message_box("enter and cancel delete", f"version {version_name} doesn't exist")

    def save_close(self, file_name=None, cancel_save=0):
        if file_name == None:
            self.full_path = self.default_file_path +  "list_" + self.default_file_name + ".xlsx"
            pass
        else:
            self.full_path = f"{self.default_file_path}list_{file_name}.xlsx"
            pass
        if cancel_save == 0 :
            self.wb.save(self.full_path)
        self.wb.close()
        self.app.quit()

    def auto_update(self, file_list0, version_name0, version_comment0, file_name0=None):
        """
        auto update just one function call
        """
        self.cancel = 0
        # this contain None and other solutions
        self.open_file(file_name=file_name0)
        self.add_version(version_name=version_name0, version_comment=version_comment0, file_list=file_list0)
        self.save_close(file_name=file_name0, cancel_save=self.cancel)


    def auto_delete(self,version_name0, file_name0=None):
        """
        auto delete just one function call
        """
        self.cancel = 0
        # this contain None and other solutions
        self.open_file(file_name=file_name0)
        self.delete_version(version_name=version_name0)
        self.save_close(file_name=file_name0, cancel_save=self.cancel)

    def message_box(self, content_str, title_str, box_type=0):
        '''
        message box function
        auto_exception is for waveform capture, will bypass fully auto setting in global setting \n
        boxtype(mpaaed with return value): 0-only confirm\n
        1-confirm: 1, cancel: 2
        2-stop: 3, re-try: 4, skip: 5
        3-yes: 6, no: 7, cancel: 2
        4-yes: 6, no: 7
        '''
        content_str = str(content_str)
        title_str = str(title_str)
        msg_res = 7

        msg_res = win32api.MessageBox(0, content_str, title_str, box_type)
        # 0 to 3 is different type of message box and can sen different return value
        # detail check on the internet
        print('msg box call~~ ')
        print('P.S Grace is cute! ~ ')

        return msg_res

# Testing code
if __name__ == "__main__":

    # overall control will be put at the other file
    test_index = 1

    # 初始化 version_file_update 對象
    vf_update = version_file_update()

    if test_index == 0 :

        # 假定Excel文件名為 'test.xlsx'，位於當前目錄
        file_path = "G:/我的雲端硬碟/py_google/file_list_free.xlsx"

        # # 初始化 version_file_update 對象
        # vf_update = version_file_update()

        # 打開 Excel 文件並加載索引
        vf_update.open_file(file_path)

        # 假定要選擇的版本名為 'Ver_1.0'
        version_to_select = "Ver_1.0"
        selected_version_content = vf_update.version_select(version_to_select)
        print(f"內容於 {version_to_select} 版本中：")
        for row_index, content in selected_version_content.items():
            print(f"{row_index}: {content}")

        # 添加一個新版本
        new_version_name = "Ver_1.3"
        new_version_comment = "comments"
        new_file_list = {"main.py": "內容1", "file_2": "內容2", "new_file": "新檔案的內容"}
        vf_update.add_version(new_version_name, new_version_comment, new_file_list)

        # 刪除一個版本
        version_to_delete = "Ver_1.1"
        vf_update.delete_version(version_to_delete)

        # 儲存並關閉 Excel 文件
        vf_update.save_close()

        print("測試完成，請檢查 Excel 文件以確認變更。")

        pass

    elif test_index == 1 :
        # full pack excel updater

        # 添加一個新版本
        new_version_name = "Ver_1.3"
        new_version_comment = "comments"
        new_file_list = {"main.py": "內容13", "file_2": "內容2", "new_file": "new_content"}
        vf_update.auto_update(new_file_list, new_version_name, new_version_comment, file_name0=None)


        # 添加一個新版本
        new_version_name = "Ver_1.0"
        new_version_comment = "comment0"
        new_file_list = {"main.py": "內容10", "file_2": "內容2", "new_file": "new_content"}
        vf_update.auto_update(new_file_list, new_version_name, new_version_comment, file_name0=None)


        # 添加一個新版本
        new_version_name = "Ver_1.2"
        new_version_comment = "comment2"
        new_file_list = {"main.py": "內容1.2", "file_2.2": "內容22", "new_file": "new_content2"}
        vf_update.auto_update(new_file_list, new_version_name, new_version_comment, file_name0=None)


        vf_update.auto_delete(version_name0="Ver_1.3",file_name0=None)
        vf_update.auto_delete(version_name0="Ver_1.2",file_name0=None)
        vf_update.auto_delete(version_name0="Ver_1.2",file_name0=None)
