from http.server import BaseHTTPRequestHandler
from os import curdir, sep
from os.path import splitext


class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            if self.path.endswith('.html'):
                mimetype = 'text/html'
            elif self.path.endswith('.jpg'):
                mimetype = 'image/jpg'
            elif self.path.endswith('.png'):
                mimetype = 'image/png'
            elif self.path.endswith('.gif'):
                mimetype = 'image/gif'
            elif self.path.endswith('.js'):
                mimetype = 'application/javascript'
            elif self.path.endswith('.css'):
                mimetype = 'text/css'
            elif self.path.endswith('.ico'):
                mimetype = 'image/ico'
            elif self.path.endswith('.ttf'):
                mimetype = 'font/ttf'
            elif self.path.endswith('woff'):
                mimetype = 'font/woff'
            else:
                mimetype = 'text/html'

            path_root, ext = splitext(self.path)
            if not ext:
                mimetype = 'text/html'
                self.path = self.path + '.html'

            if "image" or "font" in mimetype:
                f = open(curdir + sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(bytes(f.read()))
                f.close()
            else:
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(bytes(f.read(), encoding='utf-8'))
                f.close()

            return
        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)
        except UnicodeDecodeError:
            self.send_error(500, 'Decode error: %s' % self.path)
