#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import eventlet
from eventlet import wsgi
import httplib
import ftplib
import urllib
import SocketServer
import BaseHTTPServer
import time
import unicodedata
import Queue
from threading import Thread


class PosDisplay(object):

    def __init__(self):
        #self.ser = serial.Serial(2,baudrate=9600,bytesize=8, parity='N', timeout = None, stopbits=2, xonxoff=1, rtscts=1)
        #self.ser = serial.Serial(2,baudrate=9600,bytesize=8, parity='N', timeout = None, stopbits=2, xonxoff=1, rtscts=1)
        #self.ser = serial.Serial(2,baudrate=9600,parity='N',bytesize=8,stopbits=1)
        self.q = Queue.Queue()
        self.ser = serial.Serial(2,baudrate=9600)
        time.sleep(0.02)
        self.ser.write(" "*40)
        time.sleep(0.02)
        self.ser.write("OpenERP 6.1\r\n")
        self.prev1 = " "*19
        self.prev2 = " "*19
        t = Thread(target=self.worker)
        t.daemon = True
        t.start()
        for each in "PDVAL\r\n":
            self.ser.write(each)
            time.sleep(0.2)

        #self.ser.write(" "*40)
        #self.enviar_a_leds(u"OpenERP 6.1","PDVAL S.A.",0.5)

    def enviar_a_leds(self,linea1,linea2):
#        self.ser.write(" "*40)
        self.ser.write(linea1[:19]+"\r\n")
        time.sleep(0.01)
        self.ser.write(linea2[:19]+"\r\n")
        time.sleep(0.01)
        self.ser.flush()
        #for each in linea2[:18]+"\r\n":
        #    self.ser.write(each)

    
    def bridge(self, env, start_response):
        self.q.put(env['PATH_INFO'][1:])
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['OK\r\n']

    def worker(self):
        while True:
            trabajo = self.q.get()
            linea1,linea2 = trabajo.split("___") 

            for each in range(20):
                render1 = self.prev1[each:-1]+linea1[:20-(20-each)]+" "
                if len(render1)<19:
                    espacio_render1 = " "*(19-len(render1))
                else:
                    espacio_render1 = ""
                render2 = self.prev2[each:-1]+linea2[:20-(20-each)]+" "
                if len(render1)<19:
                    espacio_render2 = " "*(19-len(render2))
                else:
                    espacio_render2 = ""
                print render1
                print render2

                self.enviar_a_leds(render1,render2)
            self.prev1 = render1+" "*(19-len(render1))
            self.prev2 = render2+" "*(19-len(render2))

            self.q.task_done()
        

    def run(self):
        wsgi.server(eventlet.listen(('', 8100)), self.bridge)
        self.ser.close()

if __name__ == "__main__":
    pos_display = PosDisplay()
    pos_display.run()
