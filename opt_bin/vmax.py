#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import serial
import glob
import time

estados = { '0':' - ',
            '1':'En espera',
            '2':'Inicio de venta',
            '3':'Venta',
            '4':'Subtotal',
            '5':'Fin Venta',
            '6':'No Fiscal',
            '7':'Programacion',
            '8':'Error',
            '9':'Inicio Devol.',
            '10':'Devolucion',
            '\x15':'ERROR',
            '\x16':'VALIDO'
          }



def hex2int(number):
    return int('0x'+number.encode('hex'),16)

def check_bandera(number,pos):
    return hex2int(number) & (1 << (pos-1))

class Vmax:
    def __init__(self):
        possible_ports = glob.glob('/dev/ttyS*')
        for each in ['/dev/ttyUSB0']+range(0,6):
            try:
                print "Intentando conectar a",each
                self.ser = serial.Serial(port=each, \
                                         baudrate=9600, \
                                         bytesize=serial.EIGHTBITS, \
                                         parity=serial.PARITY_NONE, \
                                         stopbits=serial.STOPBITS_ONE, \
                                         timeout=1, xonxoff=False, \
                                         rtscts=False, \
                                         writeTimeout=None, \
                                         dsrdtr=False)
                break
            except IOError:
                print "Could not open port",each


    def estado(self):
        """ Estatus de Impresora
            Codigo: 5f
            Recibe:
            STX
            0) CK_STI status de inicialización,
            1) CK_STV status de venta, 
            2) CK_IMP status de impuesto, 
            3) CK_PRT de la impresora, 
            4) CK_INT internos, 
            5) CK_SI2 de inicialización 2 
            6) ESTADO actual
            7) CK_VAL validación.
            ETX
            También envía el estado actual de la impresora

            Modifica la Bandera: Comprobante fiscal abierto (activa)
            Estado permitido: Espera
            Estado actual:  Inicio de Venta
                                            Inicio de Devolucion
            """
        self.ser.write('\x02\x5f\x03')
        self.ser.flush()
        try:
            respuesta = self.ser.read(10)
            revisando = respuesta [1]
            print "STATUS INICIALIZACION"
            print "====================="
            print "- Inicialización:"
            print "  1:Dentro inicialización" if check_bandera(revisando,6) else "  0:Fuera Inicialización"
            print "- Reloj:"
            print "  1:Detenido" if check_bandera(revisando,4) else "  0:Normal"
            print "- Fecha invalida:"
            print "  1:Invalida" if check_bandera(revisando,3) else "  0:Valida"
            print "- Linea header:"
            print "  1:Invalida" if check_bandera(revisando,2) else "  0:Valida"
            print "- Primera Inicializacion realizada"
            print "  1:Realizada" if check_bandera(revisando,1) else "  0:Sin Realizad"

            revisando = respuesta [2]
            print "\nSTATUS DE VENTA"
            print "==============="
            print "- Comprobante fiscal abierto:"
            print "  1:Comprobante fiscal abierto" if check_bandera(revisando,7) else \
                    "  0:No hay comprobante fiscal abierto"
            print "- Comando de venta efectuado:"
            print "  1:Articulo vendido" if check_bandera(revisando,6) else "  0:Articulo no vendido"
            print "- Subtotal Realizado:"
            print "  1:Realizado" if check_bandera(revisando,5) else "  0:No Realizado"
            print "- Anulacion de pago:"
            print "  1:Anulacion de pago" if check_bandera(revisando,4) else "  0:Otra operacion"
            print "- Comando de pago efectuado:"
            print "  1:Efectuado" if check_bandera(revisando,3) else "  0:No efectuado"
            print "- Comprobante NO Fiscal abierto "
            print "  1:Comprobante NO Fiscal abierto" if check_bandera(revisando,2) else \
                    "  0:No hay comprobante no Fiscal en curso"
            print "- Periodo de Ventas Empezado"
            print "  1:Periodo comenzado" if check_bandera(respuesta[1],2) else "  0:Periodo nuevo"


            revisando = respuesta [3]
            print "\nSTATUS DE IMPUESTO"
            print "- Reporte X:"
            print "  1:Reporte X" if check_bandera(revisando,7) else "  0:Otro Reporte"
            print "- Anulacion de Articulo:"
            print "  1:Anulacion" if check_bandera(revisando,6) else "  0:Otra operacion"
            print "- Articulo exento de Impuesto:"
            print "  1:Articulo Extento" if check_bandera(revisando,5) else "  0:Articulo no exento"
            print "- Reporte Z:"
            print "  1:Reporte Z" if check_bandera(revisando,4) else "  0:Otro reporte"
            print "- Tasa de impuesto 3:"
            print "  1:Impuesto 3" if check_bandera(revisando,3) else "  0:Otro impuesto"
            print "- Tasa de impuesto 2:"
            print "  1:Impuesto 2" if check_bandera(revisando,2) else "  0:Otro impuesto"
            print "- Tasa de impuesto 1:"
            print "  1:Impuesto 1" if check_bandera(revisando,1) else "  0:Otro impuesto"


            revisando = respuesta [4]
            print "\nSTATUS DE IMPUESTO"
            print "===================="
            print "- Memoria fiscal no conectada:"
            print "  1:No conectada" if check_bandera(revisando,7) else "  0:Conectada"
            print "- Memoria fiscal agotada:"
            print "  1:Agotada" if check_bandera(revisando,6) else "  0:No agotada"
            print "- Memoria de auditoria conectada:"
            print "  1:No conectada" if check_bandera(revisando,5) else "  0:Conectada"
            print "- Memoria auditoria agotada:"
            print "  1:Agotada" if check_bandera(revisando,4) else "  0:No agotada"
            print "- Impresora fuera de linea o con la tapa levantada:"
            print "  1:Fuera de linea" if check_bandera(revisando,3) else "  0:En linea"

            revisando = respuesta [5]
            print "\nSTATUS INTERNO"
            print "===================="
            print "- Descuento sobre el total:"
            print "  1:Descuento sobre el total" if check_bandera(revisando,7) else "  0:Otra operacion"
            print "- Descuento sobre articulo:"
            print "  1:Descuento sobre articulo" if check_bandera(revisando,6) else "  0:Otra operacion"
            print "- Reporte de Memoria:"
            print "  1:Realizando reporte de memoria" if check_bandera(revisando,5) else "  0:En otra operacion"
            print "- Primer articulo vendido:"
            print "  1:Primer articulo vendido" if check_bandera(revisando,4) else \
                    "  0:Primer articulo sin vender"
            print "- Devolucion:"
            print "  1:Efectuada" if check_bandera(revisando,3) else "  0:No Efectuada"
            print "- Pago parcial realizado:"
            print "  1:Realizado" if check_bandera(revisando,2) else "  0:No Realizado"
            print "- Pago completo realizado:"
            revisando = respuesta [6]
            print "\nSTATUS INICIALIZACION"
            print "===================="
            print "- Impuesto Incluido:"
            print "  1:Incluido" if check_bandera(revisando,7) else "  0:Excluido"
            print "- Cerrando Ticket:"
            print "  1:Cerrando" if check_bandera(revisando,6) else "  0:En otra operacion"

            revisando = respuesta [6]
            print "\nSTATUS INICIALIZACION"
            print "===================="
            print "- Impuesto Incluido:"
            print "  1:Incluido" if check_bandera(revisando,7) else "  0:Excluido"
            print "- Cerrando Ticket:"
            print "  1:Cerrando" if check_bandera(revisando,6) else "  0:En otra operacion"


            print "\nSTATUS GENERAL"
            print "===================="
            print " ",estados[respuesta[7]]
        except:
            print "Status error"




    def abrir_comprobante_fiscal(self):
        """Abrir comprobante fiscal
            Modifica la Bandera: Comprobante fiscal abierto (activa)
            Estado permitido: Espera
            Estado actual:  Inicio de Venta
                            Inicio de Devolucion
            """
        self.ser.write('\x02\x4c'+'00'+'\x03')
        time.sleep(0.3)
        self.ser.flush()
        time.sleep(4)

    def abrir_devolucion_fiscal(self):
        """Abrir comprobante fiscal
            Modifica la Bandera: Comprobante fiscal abierto (activa)
            Estado permitido: Espera
            Estado actual:  Inicio de Venta
                            Inicio de Devolucion
            """
        self.ser.write('\x02\x4c'+'02'+'\x03')
        time.sleep(0.3)
        self.ser.flush()
        time.sleep(4)



    def reset(self):
        self.ser.write('\x02\x62\x03')
        time.sleep(0.2)
        self.ser.flush()
        time.sleep(4)



    def abrir_comprobante_no_fiscal(self):
        """Abrir comprobante no fiscal
            """
        self.ser.write('\x02\x53\x03')
        time.sleep(0.3)
        self.ser.flush()


    def linea_en_blanco(self):
        """Deja una linea en blanco
            """
        self.ser.write('\x02\x53\x03')
        time.sleep(0.3)
        self.ser.flush()


    def abrir_gaveta(self):
        self.ser.write('\x02\x5d\x03')
        time.sleep(0.3)
        self.ser.flush()


    def escribir_linea(self,cadena):
        self.ser.write('\x02\x56'+cadena+'\x03')
        self.ser.flush()
        time.sleep(0.3)


    def abrir_nota(self):
        """Abrir nota de credito
            Modifica la Bandera: Comprobante fiscal abierto (activa)
            Estado permitido: Espera
            Estado actual:  Inicio de Venta
                                            Inicio de Devolucion
            """
        self.ser.write('\x02\x4c\xFF\x02\x03')

    def subtotal(self):
        """Calcular subtotal de la venta
            """
        self.ser.write('\x02'+'Ox'+'\x03')
        self.ser.flush()
        time.sleep(0.3)

    def anular_comprobante(self):
        """Anular comprobante fiscal en curso
            """
        self.ser.write('\x02\x51\x03')
        time.sleep(0.3)
        self.ser.flush()

    def cerrar_comprobante(self):
        """Cerrar un comprobante fiscal en curso si se ha realizado un pago completo
            """
        self.ser.write('\x02\x4D\x03')
        time.sleep(0.3)
        self.ser.flush()
        time.sleep(3)

    def imprimir_z(self):
        self.ser.write('\x02\x5a\x03')

    def imprimir_x(self):
        self.ser.write('\x02\x58\x03')

    def venta_articulo(self,descripcion,precio,impuesto='1'):
        """Venta de articulo
            codigo: 4e
            1:      1=Venta  0=Anulacion
            20:     Descripcion
            10:     Precio
            1:      Impuesto 0=Exento 1     


            TODO: Optimizar para impresion rapida
            """

        comando_descripcion = descripcion[:20]+" "*(20-len(descripcion))
        precio_limpio = precio.replace('.','').replace(',','')
        comando_precio = "0"*(10-len(precio_limpio))+precio_limpio[:10]
        self.ser.write('\x02\x4E'+'1'+comando_descripcion+comando_precio+impuesto+'\x03')
        self.ser.flush()
        time.sleep(0.33)

    def anulacion_articulo(self,descripcion,precio,impuesto='1'):
        """Venta de articulo
            codigo: 4e
            1:      1=Venta  0=Anulacion
            20:     Descripcion
            10:     Precio
            1:      Impuesto 0=Exento 1     


            TODO: Optimizar para impresion rapida
            """

        comando_descripcion = descripcion[:20]+" "*(20-len(descripcion))
        precio_limpio = precio.replace('.','').replace(',','')
        comando_precio = "0"*(10-len(precio_limpio))+precio_limpio[:10]
        self.ser.write('\x02\x4E'+'0'+comando_descripcion+comando_precio+impuesto+'\x03')
        self.ser.flush()
        time.sleep(0.3)


    def devolucion_articulo(self,descripcion,precio,impuesto='1'):
        """Venta de articulo
            codigo: 4e
            1:      1=Venta  0=Anulacion
            20:     Descripcion
            10:     Precio
            1:      Impuesto 0=Exento 1     


            TODO: Optimizar para impresion rapida
            """

        comando_descripcion = descripcion[:20]+" "*(20-len(descripcion))
        precio_limpio = precio.replace('.','').replace(',','')
        comando_precio = "0"*(10-len(precio_limpio))+precio_limpio[:10]
        self.ser.write('\x02\x52'+'1'+comando_descripcion+comando_precio+impuesto+'\x03')
        self.ser.flush()
        time.sleep(0.33)




    def pago(self,descripcion,monto):
        """ Efectuar un pago
            codigo: 50 
            """
        print "efectuando pago",descripcion,monto
        time.sleep(2)
        comando_descripcion = descripcion[:20]+" "*(20-len(descripcion))
        monto_limpio = monto.replace('.','').replace(',','')
        comando_monto = "0"*(12-len(monto_limpio))+monto_limpio[:12]
        self.ser.write('\x02\x50\x01'+comando_descripcion+comando_monto+'\x03')
        self.ser.flush()
        time.sleep(2)


if __name__ == '__main__':
    impresora = Vmax()
    impresora.estado()
    print "reset"
    impresora.reset()
    print "abriendo comprobante"
    impresora.abrir_comprobante_fiscal()
    impresora.estado()
    for each in range(100):
        print 'prueba'+str(each)+" "+str(each*100)
        impresora.venta_articulo('prueba'+str(each),str(each*100))
        if each%10==0:
            time.sleep(1)
    #impresora.venta_articulo('prueba'+str(each)+'exento',str(each*100+50),impuesto='0')
    time.sleep(2)
    print "Subtotal"
    impresora.subtotal()
    impresora.pago('Efectivo','5000000')
    impresora.escribir_linea('Gracias por su compra.')
    impresora.escribir_linea('Hasta luego.')
    impresora.cerrar_comprobante()
