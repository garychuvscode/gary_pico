import network
import socket
import time
from machine import Pin

# fmt: off

class WiFiControl:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.led = Pin("LED", Pin.OUT)
        self.stateis = "LED is OFF"

    @staticmethod
    def html_config(state):
        return """<!DOCTYPE html>
        <html>
            <head>
                <title>Pico W</title>
            </head>
            <body>
                <h1>Pico W</h1>
                <button onclick="location.href='/light_on'">LED On</button>
                <button onclick="location.href='/light_off'">LED Off</button>
                <p>{}</p>
            </body>
        </html>
        """.format(state)
        '''
        for the htmp input, need to be causion for the reserve words:
        <button onclick="location.href='/light/on'">LED On</button>
        '/light/on' => this may cause the request function error
        '''

    def connect_to_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print("waiting for connection...")
            self.led.value(1)
            time.sleep(1)
            self.led.value(0)
            time.sleep(1)
        if wlan.status() != 3:
            raise RuntimeError("network connection failed")
        else:
            print("connected")
            status = wlan.ifconfig()
            print("ip =", status[0])

    def wifi_main(self):
        addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        print("listening on", addr)
        while True:
            try:
                cl, addr = s.accept()
                print("client connected from", addr)
                request = cl.recv(1024).decode("utf-8")
                print(f'request is :\n{request}\n')
                if self.stateis == "LED is OFF":
                    led_on = request.find("/light_on")
                    # this will cause searching error, don't use this one
                    # need to change at the search side also
                    # led_on = request.find("/light/on")
                    led_off = -1
                if self.stateis == "LED is ON":
                    led_off = request.find("/light_off")
                    # led_on = request.find("/light/off")
                    led_on = -1
                print("led on =", led_on)
                print("led off =", led_off)
                if led_on != -1:
                    print("Toggle LED on")
                    self.led.value(1)
                    self.stateis = "LED is ON"
                if led_off != -1:
                    print("Toggle LED off")
                    self.led.value(0)
                    self.stateis = "LED is OFF"
                response = self.html_config(self.stateis)
                cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
                cl.send(response)
                cl.close()
            except OSError as e:
                cl.close()
                print("connection closed")
                pass

            pass

        # end of wifi main
        pass

    def terminal(self):
        """Simulate a terminal to interact with ESP32."""
        print("Enter commands to send AT commands directly to ESP32.")
        print("Enter 'exit' to exit the terminal.")

        while True:
            user_input = input(">> ").strip()

            if user_input.lower() == "exit":
                print("Exiting terminal.")
                break
            elif user_input.startswith("fun;"):
                # 240225 this can be reserve for future use
                # If the input starts with "fun;", treat it as a class method
                method_name = user_input[len("fun;") :]
                try:
                    getattr(self, method_name)()
                except AttributeError:
                    print("Invalid command. Method not found.")
            else:
                # general case is a class method
                method_name = user_input
                try:
                    getattr(self, method_name)()
                except AttributeError:
                    print("Invalid command. Method not found.")


# Testing code
if __name__ == "__main__":

    # 初始化並啟動 WiFi 控制
    wifi_control = WiFiControl("PY Chu", "0294475990")
    wifi_control.connect_to_wifi()
    wifi_control.wifi_main()
