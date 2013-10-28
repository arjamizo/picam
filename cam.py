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
  def serve_content(self,data):
        self.send_response(200)
        self.send_header("Content-Length", len(data))
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()
        self.wfile.write(data);
  def serverStart(self): 
    ret=""
    ret+="system.os.execute(sudo motion -n);"
    print ret
    return ret+"OK"
  def serverStop(self): 
    ret=""
    ret+="system.os.execute(killall motion);"
    print ret
    return ret+"OK";
  def do_GET(self): 
    if len(self.path.split('?',1))>1:
      arg=self.path.split('?',1)[1]
      args=arg.split('&')
      cmd=args[0].split('=',1)
      print "arg=%s args=%s cmd=%s" % (arg, args, cmd)
      if args[0]=='lastsnap':
        self.serve_file('/tmp/motion/lastsnap.jpg');
      elif cmd[0]=='cmd':
        ret=("executing "+cmd[1])
        fnc=({ #http://stackoverflow.com/a/60211/781312
        'serverStop': self.serverStop
        ,'serverStart': self.serverStart
        }[cmd[1]])
        ret+=fnc()
        self.serve_content(ret)
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
    port = 8000
server_address = ('0.0.0.0', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
