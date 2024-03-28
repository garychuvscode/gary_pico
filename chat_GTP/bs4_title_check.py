from bs4 import BeautifulSoup
import requests

class GoogleDriveLinkParser:
    def get_file_name_from_link(self, drive_link):
        """
        從Google Drive分享連結中獲取文件名稱。
        這個函數將解析HTML頁面以尋找<title>標籤，然後提取文件名。

        Args:
            drive_link (str): Google Drive分享連結。

        Returns:
            str: 文件名稱，若無法獲取則返回None。
        """
        try:
            response = requests.get(drive_link)
            soup = BeautifulSoup(response.content, "html.parser")
            title_element = soup.find("title")
            
            if title_element:
                # 假定標題的格式是 "文件名 - Google 雲端硬盤"
                full_title = title_element.text.strip()
                # 這裡使用了split並選擇第一個元素，它應該是文件名
                file_name = full_title.split(' - ')[0]
                return file_name
            else:
                return None
        except Exception as e:
            print(f'Error: {e}')
            return None

if __name__ == "__main__":
    # 測試函數
    parser = GoogleDriveLinkParser()
    drive_link = "https://drive.google.com/file/d/135qWkaSVnfPvoe9DF4w-KlG1lwtTEtEQ/view?usp=drive_link"
    file_name = parser.get_file_name_from_link(drive_link)
    print(f'File Name: {file_name}')
    #end_of_main
