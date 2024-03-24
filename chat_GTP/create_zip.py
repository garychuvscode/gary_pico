import zipfile
import os


def exe_to_zip(exe_file, zip_file):
    with open(exe_file, "rb") as f:
        exe_data = f.read()

    with zipfile.ZipFile(zip_file, "w") as zipf:
        zipf.writestr(os.path.basename(exe_file), exe_data)


if __name__ == "__main__":
    exe_file = "your_executable.exe"
    zip_file = "output.zip"
    exe_to_zip(exe_file, zip_file)
