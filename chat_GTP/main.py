import sys
import machine
import utime

# ===== the only LDE on PICO, reserve for LED
led = machine.Pin(25, machine.Pin.OUT)


def led_toggle(duration=0.1):
    """
    LED toggle function, once receive command toggle,
    and duration is changeable, based on special command
    """
    led.value(1)
    utime.sleep(duration)
    led.value(0)
    utime.sleep(duration)
    pass


led_toggle(duration=0.3)
led_toggle(duration=0.3)
led_toggle(duration=0.3)
led_toggle(duration=0.3)
x = input()


if x == "gary_pico":
    # 添加模块所在目录到 sys.path
    # this seems not going to be the way to prevent copy
    print(f"input library settings:")
    x = input()
    #  x should be 'sys.path.append("grace")'
    exec(x)
else:
    # no path
    pass

try:
    # 导入模块
    import sub_main as m

    # 使用模块中的功能
    # m.my_function("hi, grace")
    m.pico_grace.pico_emb_main()

except:
    while 1:
        led_toggle()
