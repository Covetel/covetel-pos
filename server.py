import serial
import eventlet
from eventlet import wsgi
import httplib
import ftplib
import urllib
import SocketServer
import BaseHTTPServer
from vmax import Vmax



class PosPrintServer(object):
    def __init__(self):
        self.impresora = Vmax()

    def bridge(self, env, start_response):

        comando,argumentos= env['PATH_INFO'][1:].split("___")
        argumentos = argumentos.split('_-_')
        if comando == 'INICIAR':
            print "Enviando comando de RESET"
            self.impresora.reset()

        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['OK\r\n']

    def run(self):
        wsgi.server(eventlet.listen(('', 8200)), self.bridge)
        self.ser.close()

if __name__ == "__main__":
    pos_printer_server = PosPrintServer()
    pos_printer_server.run()
