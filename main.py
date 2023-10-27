import machine
import utime

import test as t

# Define the LED pin
led = machine.Pin(25, machine.Pin.OUT)

# Blink the LED in a loop

while True:
    led.toggle()  # Toggle the LED state (on/off)
    utime.sleep(0.5)  # Sleep for 1 second
    led.toggle()  # Toggle the LED state (on/off)
    utime.sleep(0.5)  # Sleep for 1 second
    led.toggle()  # Toggle the LED state (on/off)
    utime.sleep(0.5)  # Sleep for 1 second
    led.toggle()  # Toggle the LED state (on/off)
    utime.sleep(0.5)  # Sleep for 1 second
    t.test_lde()
