import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from os.path import splitext

ext_path = ''


class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if ext_path == '.':
            self.path = self.path.lstrip('/')
        else:
            self.path = ext_path.rstrip('/') + self.path
        if self.path.endswith('/') or self.path == '':
            self.path = ext_path.rstrip('/') + '/index.html'

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
                f = open(self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(bytes(f.read()))
                f.close()
            else:
                f = open(self.path)
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


class WebServer:
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        global ext_path
        ext_path = path
        self.server = HTTPServer((self.host, int(self.port)), SimpleServer)

    def start_server(self):
        print('Running web server on http://' + self.host + ':' + self.port + '(Press CTRL+C to quit)')
        self.server.serve_forever()

    def stop_server(self):
        self.server.socket.close()
        sys.exit()
