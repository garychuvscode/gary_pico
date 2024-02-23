import network
import socket
import time

from machine import Pin

led = Pin(25, Pin.OUT)

ssid = 'PY Chu'
password = '0294475990'

# Initialize stateis variable with default value
stateis = "LED is OFF"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html>
<html>
    <head>
        <title>Pico W</title>
    </head>
    <body>
        <h1>Pico W</h1>
        <button onclick="location.href='/light/on'">LED On</button>
        <button onclick="location.href='/light/off'">LED Off</button>
        <p>%s</p>
    </body>
</html>
"""

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Initialize stateis variable with default value
stateis = "Unknown"

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        led_on = request.find('/light/on')
        led_off = request.find('/light/off')
        print('led on = ' + str(led_on))
        print('led off = ' + str(led_off))

        # Toggle LED based on request URL
        if led_on != -1:
            print("Toggle LED on")
            led.value(1)
            stateis = "LED is ON"

        if led_off != -1:
            print("Toggle LED off")
            led.value(0)
            stateis = "LED is OFF"

        response = html % stateis

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')