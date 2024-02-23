import bluetooth
import random
import struct
import time
from micropython import const
from machine import Timer

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)

'''
This BLE class provides basic functionalities for initializing BLE, 
advertising, and handling connections in MicroPython on Raspberry Pi Pico W.

Attributes:
- ble (bluetooth.BLE): The BLE interface.
- led (Pin): LED pin to indicate BLE status.
- timer (Timer): Timer for updating LED status.
- connected (bool): Connection status flag.
'''

class PicoW_BLE:
    def __init__(self, name):
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self.advertising = False
        self.connected = False
        self.name = name
        self._advertise()

    def _advertise(self, interval_us=500000):
        '''
        Starts advertising the device with the specified name and interval.

        Args:
        - interval_us (int): Advertising interval in microseconds.
        '''
        self.ble.gap_advertise(interval_us, adv_data=self._adv_data())

    def _adv_data(self):
        '''
        Constructs the advertising payload with the device name.

        Returns:
        - bytes: The advertising payload.
        '''
        return bytearray(struct.pack("B", len(self.name) + 1) + struct.pack("b", 0x09) + self.name.encode())

    def ble_irq(self, event, data):
        '''
        Handles BLE IRQ events for connections and disconnections.

        Args:
        - event: The IRQ event.
        - data: The event data.
        '''
        if event == _IRQ_CENTRAL_CONNECT:
            # A central device has connected to this peripheral.
            self.connected = True
            self._update_led_status()

        elif event == _IRQ_CENTRAL_DISCONNECT:
            # A central device has disconnected from this peripheral.
            self.connected = False
            self._update_led_status()
            # Automatically restart advertising to allow a new connection.
            self._advertise()

    def _update_led_status(self):
        '''
        Updates the LED status based on the BLE connection.
        '''
        if self.connected:
            # Implement LED on logic here
            pass
        else:
            # Implement LED off logic here
            pass

    def print_progress_bar(self, iteration=0, total=100, prefix='Progress:', suffix='Complete', length=50, fill='#'):
        '''
        printout the prograss of the status 
        '''
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
        if iteration == total:
            print()

# Testing code
if __name__ == "__main__":
    # Replace 'PicoW_BLE_Test' with your desired BLE device name
    ble_device = PicoW_BLE('PicoW_BLE_Test')
    x = 0 
    while True:
        ble_device.print_progress_bar(iteration=x)
        if x > 99: 
            x = 0 
        else: 
            x = x + 1
        # Implement your BLE service logic here
        # For example, you could read sensor data and send it over BLE
        time.sleep(1)  # Sleep to simulate doing work
        #end_of_loop
#end_of_main
