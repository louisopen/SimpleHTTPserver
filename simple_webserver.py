#!/usr/bin/python
#coding=utf-8
# Install in Linux bash
# Python3 –m http.server           #
# sudo pip install simple_http_server   #?
'''
python3 ./simple_webserver.py    # Run command to handle multiple GET request in the HW platform.
IE examples:
http://192.168.0.114:8000/       # Display the webpage without LED status
http://192.168.0.114:8000/on     # Turn on the LED and display LED is On
http://192.168.0.114:8000/off    # Turn off the LED and display LED is off
'''
import os
import sys
import socket
import RPi.GPIO as GPIO          # Check it in your windows or Raspbian platform
from http.server import BaseHTTPRequestHandler, HTTPServer      # must be run python3 -m http.server   


class MytestHTTPServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <h1>The stepping motor control panel</h1>
            <p>Current GPU temperature is {}</p>
            <p>TEST THE LINE01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789</p>
            <p>The UART default setting is 9600,N,8,1</p>
            <form action="/" method="POST">
                Turn LED :
                <input type="submit" name="submit" value="On">
                <input type="submit" name="submit" value="Off">
                <input type="submit" name="submit" value="STOP    ">
            </form>
            <form action="/" method="POST">
                Uart On/Off :
                <input type="submit" name="submit" value="TXD">
                <input type="submit" name="submit" value="RXD">
            </form>
            </body>
            </html>
        '''
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:]).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])    # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")   # Get the data
        #post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        post_data = post_data.split("=")[1]    # Only keep the value

        # You now have a dictionary of the post data

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18,GPIO.OUT)

        if post_data == 'On':
            GPIO.output(18, GPIO.HIGH)
        else:
            GPIO.output(18, GPIO.LOW)
        print("LED is {}".format(post_data))
        self._redirect('/')      # Redirect back to the root url
        #self.wfile.write("You finished it".encode("utf-8"))

def getIP():
    myname = socket.getfqdn(socket.gethostname())
    get_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    get_s.connect(('8.8.8.8', 0))
    #ip = ('hostname: %s, localIP: %s') % (myname, get_s.getsockname()[0])
    ip = ('%s') % (get_s.getsockname()[0])
    return ip

def run():
    if sys.argv[1:]:
        host_port = int(sys.argv[1])
    else:
        host_port = 8000         # print('starting server, port', host_port)       
    host_name = getIP()          # same the localhost ip  host_name = '192.168.0.17'         
    # Server settings
    server_address = (host_name, host_port) 
    httpd = HTTPServer(server_address, MytestHTTPServer)
    #httpd = MyThreadingHTTPServer(('',8080), MytestHTTPServer)
    #httpd = MyThreadingHTTPServer(server_address, MytestHTTPServer)
    print('running server...', server_address)

    httpd.serve_forever()

if __name__ == '__main__': 
    run()