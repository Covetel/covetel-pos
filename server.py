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
        print "atendiendo:",env['PATH_INFO']

        comando= env['PATH_INFO'][1:].split("___")
        if comando[0] == 'RESET':
            print "Enviando comando de RESET"
            self.impresora.reset()
        if comando[0] == 'ABRIR1':
            print "Abriendo comprobante fiscal"
            self.impresora.abrir_comprobante_fiscal()
        if comando[0] == 'PRODUCTO':
            print "Enviando producto"
            self.impresora.abrir_comprobante_fiscal()
            self.impresora.venta_articulo(comando[1],comando[2])
        if comando[0] == 'SUBTOTAL':
            print "Enviando Subtotal"
            self.impresora.subtotal()
        if comando[0] == 'PAGO':
            print "Enviando pago"
            self.impresora.pago(comando[1],comando[2])
        if comando[0] == 'CERRAR1':
            print "Cerrando comprobante"
            self.impresora.cerrar_comprobante()



        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['OK\r\n']

    def run(self):
        wsgi.server(eventlet.listen(('', 8200)), self.bridge)
        self.ser.close()

if __name__ == "__main__":
    pos_printer_server = PosPrintServer()
    pos_printer_server.run()
