"""
this file used to transfer the file to .mpy file and put all
the file into pico with config directory
this should be run in python terminal, not pico terminal
"""

# fmt: off
import subprocess

def execute_commands(commands):
    """執行一系列系統命令"""
    for command in commands:
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        if process.returncode == 0:
            print(f"命令 '{command}' 執行成功:")
            print(process.stdout)
        else:
            print(f"命令 '{command}' 執行失敗:")
            print(process.stderr)



if __name__ == "__main__":
    # 將你想執行的命令作為列表元素
    commands = [
        "mpy-cross pico_pack/main_out.py",  # 將 example.py 轉換為 .mpy
        "ampy --port /dev/ttyACM0 put example.mpy",  # 將 example.mpy 上傳到 Pico
        # 更多命令...
    ]

    # 執行命令
    execute_commands(commands)
