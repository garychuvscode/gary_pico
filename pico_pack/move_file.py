import shutil
import os

"""
this file transfer the related file to mpy and save to the cloud folder
so just press F5 and may need to enter the version code for the next release

"""


def convert_to_mpy(file_name, file_dist):
    """
    Convert a Python file to .mpy format using mpy-cross.

    Parameters:
    file_name (str): The relative path to the Python file to be converted.
    file_dist (str): The absolute path to the destination directory.
    """
    try:
        # Get the full path of the Python file
        file_path = os.path.abspath(file_name)

        # Convert Python file to .mpy format
        os.system(f"mpy-cross {file_path}")

        # Get the name of the original file
        file_basename = os.path.basename(file_path)

        # Create the destination directory if it doesn't exist
        os.makedirs(file_dist, exist_ok=True)

        # Move the .mpy file to the destination directory
        shutil.move(f"{os.path.splitext(file_path)[0]}.mpy", file_dist)

        print("Conversion completed successfully!")
    except Exception as e:
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    file_name = "pico_pack\\main_out.py"
    file_dist = "G:\\我的雲端硬碟\\pico_release"
    convert_to_mpy(file_name, file_dist)
