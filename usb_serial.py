import time
from machine import Pin
import sys
import machine

led = Pin(0, machine.Pin.OUT)
led2 = Pin(2, machine.Pin.OUT)
led2.value(0)
led.value(0)


def led_on():
    led.value(1)


def led_off():
    led.value(0)


# ==== read string

input_string = "部分1.部分2.部分3.部分4.部分5"  # 这里有5个部分，但可以是任意数量


def string_split(string0="."):
    # 使用 str.split() 分割字符串
    parts = input_string.split(".")

    # 将部分存储在列表中
    part_list = parts

    # 打印各个部分
    for i, part in enumerate(part_list, start=1):
        print(f"部分 {i}: {part}")

    return part_list


# ==== universal input string

while True:
    # read a command from the host
    v = sys.stdin.readline().strip()

    # perform the requested action
    if v.lower() == "on":
        led_on()
        print("Turned on!")
    elif v.lower() == "off":
        led_off()
        print("Turned off!")
