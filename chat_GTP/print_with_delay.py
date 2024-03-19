import time

def print_with_delay(text, delay):
    """
    Print each character of the text with a specified delay between characters.

    Parameters:
    text (str): The text to be printed.
    delay (float): The delay (in seconds) between each character.
    """
    for char in text:
        print(char, end='', flush=True)  # end='' 表示不換行，flush=True 表示立即輸出至終端
        time.sleep(delay)  # 控制延遲

# Example usage
if __name__ == "__main__":
    text = "Hello, World!"
    delay = 0.1  # 設定延遲為 0.1 秒
    print_with_delay(text, delay)
