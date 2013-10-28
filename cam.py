import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

i=0;
lastans=""
class myHandler(SimpleHTTPRequestHandler): 
  def serve_file(self, file, nocache=1): 
      content=""
      with open(file, 'r') as content_file:
        content = content_file.read()
      self.send_response(200)
      self.send_header("Content-Length", len(content))
      if nocache:
        self.send_header("Last-Modified", self.date_time_string())
      self.end_headers()
      self.wfile.write(content);
  def do_GET(self): 
    if len(self.path.split('?',1))==2:
      arg=self.path.split('?',1)[1]
      print arg
      if arg=='lastsnap':
        self.serve_file('/tmp/motion/lastsnap.jpg');
      else: 
        data=arg
        self.send_response(200)
        self.send_header("Content-Length", len(data))
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()
        self.wfile.write(data);
    # except Exception, e:
    else:
      print self.path
      SimpleHTTPRequestHandler.do_GET(self)
      # raise e

HandlerClass = myHandler
ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8080
server_address = ('0.0.0.0', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
