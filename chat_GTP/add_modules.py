"""

如果我在其他目錄中存放python檔案, 是否可以直接import 進來到main進行使用??
ChatGPT
在 MicroPython 中，如果你的 Python 文件（.py 文件）位于不同的目录下，你可以使用 sys.path 来告诉 MicroPython 解释器在哪里搜索模块。以下是一个简单的示例：

假设你有如下的文件结构：

markdown
Copy code
- main.py
- modules
  - mymodule.py
其中 main.py 是你的主程序文件，而 mymodule.py 是你要导入的模块。

在 main.py 中，你可以使用以下代码：

240201 note:
need a file to update code into the related directory like flash accessing
(if this will work from the pico)

"""

import sys

# 添加模块所在目录到 sys.path
sys.path.append("modules")

# 导入模块
import mymodule

# 使用模块中的功能
mymodule.my_function("hi, grace")

"""
上述代码将 modules 目录添加到 sys.path 中，这样 MicroPython 解释器就知道在这个目录下搜索模块。

在 mymodule.py 文件中，你可以定义一些功能：

python
Copy code

"""
# mymodule.py


def my_function(input):
    print(f"Hello from mymodule! from add_module.py {input}")


"""
这样，当你运行 main.py 时，它将成功导入 mymodule 并调用其中的功能。请确保你的模块路径正确，
并根据实际情况调整 sys.path。

"""
