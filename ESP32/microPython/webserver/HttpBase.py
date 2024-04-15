"""
  Klasse til at håndtere HTTP kommunikation
"""
import socket
import os
import _thread


class HttpBase():
    # reference konstanter
    HTML_BASE = 'html/'
    NOT_FOUND_TEMPLATE = 'html/404.html'
    TEXT_HTML = 'text/html'
    TEXT_CSS = 'text/css'
    TEXT_JAVASCRIPT = 'text/javascript'

    def __init__(self):
        self._client = None
        self.debug = False

    def create_response(self, filename='404.html', content_type='text/html'):
        response = self.get_file(filename)
        self._client.send('HTTP/1.1 200 OK\n')
        self._client.send('Content-Type: ' + content_type + '\n')
        self._client.send('Connection: close\n\n')
        self._client.sendall(response)
        self._client.close()

    # læs filer fra lokalt fil system
    def get_file(self, filename):
        """
        Returns a file from ESP32 filesystem
        :param filename:
        :return:
        """
        try:
            filesystem = os.listdir(self.HTML_BASE)
            if filename not in filesystem:
                error = f'Error: {filename} file not found in root dir. Found: {filesystem}'
                print(error)
                return error  # TODO check it is safe to return a string instead of file
            file = open(self.HTML_BASE+filename)
            f = file.read()
            file.close()
            return f
        except Exception as e:
            return e

    def http_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 80))
        sock.listen(5)
        
        while True:
          self._client, addr = sock.accept()
          print('Client %s is connected' % str(addr))
          request = self._client.recv(1024)
          self._request = str(request)
          self.handle()

    def handle(self):
        """ Override the handler to create responses to requests.
            The request object is self._request
        """
        pass
    
    def start_http_server(self):
        # Start http thread
        _thread.start_new_thread(self.http_server, ())
        