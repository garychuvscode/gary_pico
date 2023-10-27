import machine
import utime

# Define the LED pin
led = machine.Pin(25, machine.Pin.OUT)

# Blink the LED in a loop


def test_lde1():
    x = 0

    while x < 3:
        led.toggle()  # Toggle the LED state (on/off)
        utime.sleep(3)  # Sleep for 1 second
        x = x + 1
        pass
    pass


def test_lde():
    led.toggle()
    utime.sleep(5)
    led.toggle()
    pass
