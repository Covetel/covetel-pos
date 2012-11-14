import serial
import eventlet
from eventlet import wsgi
import httplib
import ftplib
import urllib
import SocketServer
import BaseHTTPServer
from vmax import Vmax
import time
import Queue
from threading import Thread
import logging


class PosPrintServer(object):
    def __init__(self):
        logging.basicConfig(filename='/var/log/print-server.log', filemode='w',format='%(asctime)s %(message)s',level=logging.DEBUG)
        self.impresora = Vmax()
        self.q = Queue.Queue()
        t = Thread(target=self.worker)
        t.daemon = True
        t.start()
        logging.info('PosPrintServer inicializado')
        self.ser = "OK"

    def worker(self):
        while True:
            try:
                comando = self.q.get()
                comando = comando.split("___")
                try:
                    comando[2] = comando[2].split(".")[0]
                except:
                    pass

                if comando[0] == 'RESET':
                    logging.info("Enviando comando de RESET")
                    self.impresora.reset()
                if comando[0] == 'ABRIR1':
                    logging.info("Abriendo comprobante fiscal")
                    num = self.impresora.abrir_comprobante_fiscal()
                    if num != None:
                        self.ser = num 
                if comando[0] == 'ABRIR2':
                    logging.info("Abriendo devolucion fiscal")
                    self.impresora.abrir_devolucion_fiscal()
                if comando[0] == 'PRODUCTO':
                    logging.info("Enviando producto")
                    self.impresora.venta_articulo(comando[1],comando[2])
                if comando[0] == 'ANULACION':
                    logging.info("Enviando producto")
                    self.impresora.anulacion_articulo(comando[1],comando[2])
                if comando[0] == 'DEVOLUCION':
                    logging.info("Enviando producto a devolver")
                    self.impresora.devolucion_articulo(comando[1],comando[2])
                if comando[0] == 'SUBTOTAL':
                    logging.info("Enviando Subtotal")
                    self.impresora.subtotal()
                if comando[0] == 'PAGO':
                    logging.info("Enviando pago")
                    self.impresora.pago(comando[1],comando[2])
                if comando[0] == 'BLANCO':
                    self.impresora.avance_linea()
                if comando[0] == 'ESCRIBIR':
                    logging.info("ESCRIBIENDO: "+comando[1])
                    self.impresora.escribir_linea(comando[1])
                if comando[0] == 'CERRAR1':
                    logging.info("Cerrando comprobante")
                    tweet = "Felicito a los y las Graduandas del I Cohorte del Diplomado en Saberes Africanos! Viva la Madre Africa!! " 
                    self.impresora.avance_linea()
                    self.impresora.escribir_linea("@chavezcandanga:")
                    self.impresora.escribir_linea(tweet[:40])
                    self.impresora.escribir_linea(tweet[40:80])
                    self.impresora.escribir_linea(tweet[80:120])
                    self.impresora.escribir_linea(tweet[120:160])
                    
                    self.impresora.cerrar_comprobante()
                if comando[0] == 'GAVETA':
                    logging.info("Abriendo Gaveta")
                    self.impresora.abrir_gaveta()
                if comando[0] == 'REPORTEX':
                    logging.info("Enviando Reporte X")
                    self.impresora.imprimir_x()
                if comando[0] == 'REPORTEZ':
                    logging.info("Enviando Reporte Z")
                    self.impresora.imprimir_z()
            except IOError:
                logging.warning(comando[0]+' ERROR')

            self.q.task_done()

    def bridge(self, env, start_response):
        logging.info('Procesando'+env['PATH_INFO'])
        try:
            self.q.put(env['PATH_INFO'][1:])
            start_response('200 OK', [('Content-Type', 'text/plain')])
        except:
            logging.warning('Bridge ERROR processing:'+env['PATH_INFO'])
        return [str(self.ser)+'\r\n']

    def run(self):
        wsgi.server(eventlet.listen(('', 8200)), self.bridge)
        self.ser.close()

if __name__ == "__main__":
    pos_printer_server = PosPrintServer()
    pos_printer_server.run()
