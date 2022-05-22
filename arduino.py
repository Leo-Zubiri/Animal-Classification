'''
Clase, Modulo u Objeto (archivo py) 
Que simula al Arduino para no incluir todo el codigo en una plantilla
Y simplemente importar este archivo
'''
#from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
#import sys
from PyQt5 import QtWidgets
import serial

class c_arduino():
    def __init__(self):
        self.arduino = None

    def connect(self, port="COM3",btn = QtWidgets.QPushButton):        
        if self.arduino == None:
            #com = "COM" + self.txt_com.text()
            #self.txt_com.setEnabled(False)
            try:
                self.arduino = serial.Serial(port, baudrate=9600, timeout=200)
                print("Conexion Inicializada")
                btn.setText("Desconectar")

            except serial.SerialException:                                            
                msgbox = QtWidgets.QMessageBox()
                msgbox.setWindowTitle("Error de puerto")
                msgbox.setText("Intente en otro puerto diferente")        
                msgbox.exec_()   
                self.arduino = None
                btn.setText("Conectar")
            


        elif self.arduino.isOpen():
            btn.setText("Reconectar")
            self.arduino.close()
            print("Conexion Cerrada")
        else:
            btn.setText("Desconectar")
            self.arduino.open()
            print("Conexion Reconectada")


    def write(self, data):
        if not(self.verifyConnection()):
            return False

        self.arduino.write(data.encode())
        print("El dato ha sido enviado correctamente")
        return True



    def read(self):
        if not(self.verifyConnection()):
            return False

        data = self.arduino.readline().decode()
        #print("El dato ha sido leido: {}".format(data))
        return(data)



    def disconnect(self):
        if not(self.verifyConnection()):
            return True

        self.arduino.close()
        print("Se cerro Arduino con Exito")


    
    def verifyConnection(self):
        if self.arduino == None:
            #print("Aun no se ha realizado la conexion con arduino")
            return False

        if not(self.arduino.isOpen()):
            #print("La conexion esta cerrada actualmente")
            return False

        return True


    def inWaiting(self):
        if self.arduino == None:
            return False
        if not(self.arduino.isOpen()):
            #print("La conexion esta cerrada actualmente")
            return False
        return self.arduino.inWaiting()
