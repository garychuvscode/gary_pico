import machine
import utime
import time

# fmt: off

class test_obj:
    def __init__(self):
        # Define the LED pin
        self.led = machine.Pin(25, machine.Pin.OUT)
        self.gpio_0 = machine.Pin(0, machine.Pin.OUT)

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
        self.gpio_0.value(1)
        self.gpio_0.value(0)
        pass


if __name__ == "__main__":
    # testing for test_obj

    test_o = test_obj()

    test_index = 2

    if test_index == 0:
        # LDO toggle
        test_o.test_lde()

        test_o.test_lde1()

    elif test_index == 1:
        test_o.full_speed_toggle()

    elif test_index == 2:
        test_o.time_duration_testing()
