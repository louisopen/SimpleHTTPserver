"""
Install:
Python3 –m http.server           #
Pip install simple_http_server   #?

python3 simple_webserver.py      # Run command to handle multiple GET request in the HW platform.
example:
http://192.168.0.114:8000/       # Display the webpage without LED status
http://192.168.0.114:8000/on     # Turn on the LED and display LED is On
http://192.168.0.114:8000/off    # Turn off the LED and display LED is off

"""
import os
import sys
import socket
import cgi
import RPi.GPIO as GPIO          # Check it in your windows or Raspbian platform

from http.server import BaseHTTPRequestHandler, HTTPServer      # must be run python3 -m http.server   
"""
#from SimpleHTTPServer import SimpleHTTPRequestHandler, BaseHTTPServer
#HandlerClass = SimpleHTTPRequestHandler
#ServerClass  = BaseHTTPServer.HTTPServer
#Protocol     = "HTTP/1.0"
"""
"""
import socketserver  
class MyThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):  # 採用多線程執行(開啟多頁)
    pass  
"""
class MytestHTTPServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command 
            'curl -I http://server-ip-address:port' 
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        """ do_GET() can be tested using curl command 
            'curl http://server-ip-address:port' 
        """
        html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <h1>Welcome to the platform setting</h1>
            <p>Current GPU temperature is {}</p>
            <form action="/" method="POST">
                Turn LED :
                <input type="submit" name="submit" value="On">
                <input type="submit" name="submit" value="Off">
            </form>
            <form action="/" method="POST">
                Uart On/Off :
                <input type="submit" name="submit" value="On">
                <input type="submit" name="submit" value="Off">
            </form>
            </body>
            </html>
        '''
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:]).encode("utf-8"))

    def do_POST(self):
        """ do_POST() can be tested using curl command 
            'curl -d "submit=On" http://server-ip-address:port' 
        """
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
'''
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],
            }
            )
        self.send_response(200)        
        self.end_headers()        
        self.wfile.write('Client: %sn ' % str(self.client_address) )        
        self.wfile.write('User-agent: %sn' % str(self.headers['user-agent']))        
        self.wfile.write('Path: %sn'%self.path)        
        self.wfile.write('Form data:n')        
        for field in form.keys():            
            field_item = form[field]            
            filename = field_item.filename            
            filevalue  = field_item.value            
            filesize = len(filevalue)  #文件大小(字节)            
            #print len(filevalue)	   #print (filename)            
            with open(filename.decode('utf-8'),'wb') as f:                
            f.write(filevalue)
'''

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
    #host_name = '10.132.10.25'   # your Raspberry Pi IP address
    host_name = getIP()          # same the localhost ip             
    # Server settings
    server_address = (host_name, host_port) 
    httpd = HTTPServer(server_address, MytestHTTPServer)
    #httpd = MyThreadingHTTPServer(('',8080), MytestHTTPServer)
    #httpd = MyThreadingHTTPServer(server_address, MytestHTTPServer)
    print('running server...', server_address)

    #HandlerClass.protocol_version = Protocol    # used SimpleHTTPRequestHandler
    #httpd = ServerClass(server_address, HandlerClass) #used default server class
    #sa = httpd.socket.getsockname()
    #print "Serving HTTP on", sa[0], "port", sa[1], "..."

    httpd.serve_forever()

if __name__ == '__main__': 
    run()