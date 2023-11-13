import machine
import utime
import time

# fmt: off

class test_obj:
    def __init__(self):
        # Define the LED pin
        self.led = machine.Pin(25, machine.Pin.OUT)
        self.gpio_0 = machine.Pin(8, machine.Pin.OUT)

        pass

    # Blink the LED in a loop
    def test_lde1(self):
        x = 0

        while x < 3:
            # self.led.toggle()  # Toggle the LED state (on/off)
            self.led.value(1)
            utime.sleep(3)  # Sleep for 1 second
            self.led.value(0)
            utime.sleep(3)
            x = x + 1
            pass
        pass

    def test_lde(self):
        self.led.value(1)
        utime.sleep(0.5)
        self.led.value(0)
        utime.sleep(0.5)
        pass

    def full_speed_toggle(self):
        while 1:
            self.led.value(1)
            self.gpio_0.value(1)
            self.gpio_0.value(0)
            time.sleep_us(100)
            self.led.value(0)

        pass

    def time_duration_testing(self):

        while 1 :
            # self.gpio_0.value(1)
            # time.sleep_us(14)
            # self.gpio_0.value(0)
            self.gpio_ch_us()

        pass

    def gpio_ch_us(self, us=20):
        self.gpio_0.value(1)
        time.sleep_us(us)
        self.gpio_0.value(0)
        pass

    def toggle_once(self):
        self.led.value(1)
        time.sleep(0.2)
        self.led.value(0)
        pass

    def infinite_toggle(self, diration0=0.2):

        while 1 :

            x = float(input())

            self.led.value(1)
            utime.sleep(x)
            self.led.value(0)
            utime.sleep(x)

            self.led.value(1)
            utime.sleep(x)
            self.led.value(0)
            utime.sleep(x)

            self.led.value(1)
            utime.sleep(x)
            self.led.value(0)
            utime.sleep(x)

        pass

    def dedent_skip_1(self, code):
        lines = code.split('\n')
        # 计算最小缩进
        min_indent = float('inf')
        for line in lines[1:]:  # 跳过第一行，因为它通常是模块级别的缩进
            stripped = line.lstrip()
            if stripped:
                indent = len(line) - len(stripped)
                min_indent = min(min_indent, indent)

        # 移除最小缩进
        dedented_lines = [line[min_indent:] for line in lines]
        dedented_code = '\n'.join(dedented_lines)
        return dedented_code

    def dedent(self, code):
        lines = code.split('\n')
        # 计算最小缩进
        min_indent = float('inf')
        for line in lines:
            stripped = line.lstrip()
            if stripped:
                indent = len(line) - len(stripped)
                min_indent = min(min_indent, indent)

        # 移除最小缩进
        dedented_lines = [line[min_indent:] for line in lines]
        dedented_code = '\n'.join(dedented_lines)
        return dedented_code

    def execute_indented_code(self, code):
        # 获取执行上下文的缩进
        current_indent = ' ' * (len(code) - len(code.lstrip()))

        # 在代码块的每一行前添加当前缩进
        indented_code = '\n'.join([current_indent + line for line in code.split('\n')])

        # 执行代码块
        exec(indented_code)

    def toggle_once2(self):
        cmd='''
self.led.value(1)
time.sleep(0.2)
self.led.value(0)
        '''
        cmd = self.dedent(cmd)
        # to use self in exec, must have below instruction
        exec(cmd, globals(), {'self': self})

        '''
        refer to below reference, thanks for chat GTP

 如果是在class 中呼叫 exec() , 其中可以使用 相同class 內有的 method or parameter 嗎?

ChatGPT
是的，您可以在类中使用 exec()，并访问相同类内的方法或属性。在类的方法中，您可以使用 self 来引用当前实例，然后在 exec() 中使用这个实例。

以下是一个简单的示例：

        class MyClass:
    def __init__(self, value):
        self.value = value

    def execute_code(self, code):
        # 在执行时可以访问类内的属性和方法
        exec(code, globals(), {'self': self})

    def print_value(self):
        print("Current value:", self.value)

# 创建类的实例
my_instance = MyClass(42)

# 定义并执行代码块，其中访问了类的方法和属性
code_block = """
self.print_value()
self.value *= 2
self.print_value()
"""

my_instance.execute_code(code_block)

在上面的示例中，execute_code 方法使用 exec() 执行了一个代码块，
其中访问了类的方法和属性。请注意，在 exec() 中通过 globals() 和
 {'self': self} 传递了全局作用域和 self 变量，以确保代码块中能够
 访问到相应的内容。这样，您就可以在 exec() 中使用类内的方法和属性了。

        '''
        pass

    def next_function(self):

        pass


if __name__ == "__main__":
    # testing for test_obj

    test_o = test_obj()

    test_index = 6

    if test_index == 0:
        # LDO toggle
        test_o.test_lde()

        test_o.test_lde1()

    elif test_index == 1:
        test_o.full_speed_toggle()

    elif test_index == 2:
        test_o.time_duration_testing()

    elif test_index == 3:
        t = 0.1
        print(f'this is test, duration {t}')
        test_o.infinite_toggle(t)

    elif test_index == 4:
        test_o.toggle_once()

    elif test_index == 5:
        cmd = '''test_o.toggle_once()'''
        print(cmd)
        exec(cmd)

    elif test_index == 6:
        test_o.toggle_once2()
