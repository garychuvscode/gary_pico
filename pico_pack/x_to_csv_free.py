import pandas as pd
import os

def xlsx_to_csv(input_file, output_file):
    """
    Convert an Excel file to CSV format.

    Parameters:
        input_file (str): The path to the input Excel file.
        output_file (str): The path to save the output CSV file.

    Returns:
        None
    """
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(input_file)
        
        # Write the DataFrame to a CSV file
        df.to_csv(output_file, index=False, encoding="utf-8")
        
        print(f"Excel file '{input_file}' converted to CSV file '{output_file}' successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    # 確定輸入和輸出路徑為絕對路徑
    input_file = os.path.abspath("pico_pack/file_list_free.xlsx")  # 將相對路徑轉換為絕對路徑
    output_file = "G:/我的雲端硬碟/pico_release/free_version/file_list_free.csv"  # 指定絕對路徑
    
    # 呼叫函數進行轉換
    xlsx_to_csv(input_file, output_file)
    print(f'done for file_list_free.csv updated')
