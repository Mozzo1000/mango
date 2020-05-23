from http.server import BaseHTTPRequestHandler
from os import curdir, sep


class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == '/':
            self.path = '/index.html'
        try:
            sendreply = False
            if self.path.endswith('.html'):
                mimetype = 'text/html'
                sendreply = True
            if self.path.endswith('.jpg'):
                mimetype = 'image/jpg'
                sendreply = True
            if self.path.endswith('.png'):
                mimetype = 'image/png'
                sendreply = True
            if self.path.endswith('.gif'):
                mimetype = 'image/gif'
                sendreply = True
            if self.path.endswith('.js'):
                mimetype = 'application/javascript'
                sendreply = True
            if self.path.endswith('.css'):
                mimetype = 'text/css'
                sendreply = True
            if self.path.endswith('.ico'):
                mimetype = 'image/ico'
                sendreply = True
            if sendreply:
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(bytes(f.read(), encoding='utf-8'))
                f.close()
            return
        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)
