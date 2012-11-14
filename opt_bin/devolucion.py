from vmax import Vmax
import time

if __name__ == '__main__':
    impresora = Vmax()
    impresora.estado()
    print "reset"
    impresora.reset()
    print "abriendo comprobante"
    impresora.abrir_devolucion_fiscal()
    time.sleep(3)
    impresora.estado()
    for each in range(10):
        print 'prueba'+str(each)+" "+str(each*100)
        impresora.devolucion_articulo('prueba'+str(each),str(each*100))
        if each%10==0:
            time.sleep(1)
    #impresora.venta_articulo('prueba'+str(each)+'exento',str(each*100+50),impuesto='0')
    time.sleep(2)
    print "Subtotal"
    impresora.subtotal()
    impresora.pago('Efectivo','0')
    #impresora.escribir_linea('Gracias por su compra.')
    #impresora.escribir_linea('Hasta luego.')
    impresora.cerrar_comprobante()
