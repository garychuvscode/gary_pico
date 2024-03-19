import shutil
import os

def convert_to_mpy(file_name, file_dist, new_file_name=None):
    """
    Convert a Python file to .mpy format using mpy-cross and move it to the destination directory.

    Parameters:
    file_name (str): The relative path to the Python file to be converted.
    file_dist (str): The absolute path to the destination directory.
    new_file_name (str, optional): The new name for the .mpy file. If None, the original name will be used.
    """
    try:
        # Get the full path of the Python file
        file_path = os.path.abspath(file_name)
        
        # Convert Python file to .mpy format
        os.system(f'mpy-cross {file_path}')
        
        # Get the name of the original file
        file_basename = os.path.basename(file_path)
        
        # Determine the new file name
        if new_file_name is None:
            new_file_name = os.path.splitext(file_basename)[0] + '.mpy'
        
        # Create the destination directory if it doesn't exist
        os.makedirs(file_dist, exist_ok=True)
        
        # Move the .mpy file to the destination directory with the new name
        shutil.move(f'{os.path.splitext(file_path)[0]}.mpy', os.path.join(file_dist, new_file_name))
        
        print("Conversion completed successfully!")
    except Exception as e:
        print(f'Error: {e}')

# Example usage
if __name__ == "__main__":
    file_name = "pico_pack\\main_out.py"
    file_dist = "C:/gary_folder/pico_pack"
    new_file_name = "new_main_out.mpy"  # 新的檔案名稱
    convert_to_mpy(file_name, file_dist, new_file_name)
