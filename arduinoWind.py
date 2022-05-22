import sys
# Modulo/clase arduino
import arduino as ard 
import time
from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile = "arduinoWind.ui" # Nombre del archivo .ui aqui.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Área de los Signals y Configuraciones Iniciales
        self.btn_conectar.clicked.connect(self.conectar)
        #self.btn_agregar.clicked.connect(self.agregar)
        #self.btn_accion.clicked.connect(self.accion)
	 
        #Instanciamos un objeto de la clase marduino
        self.arduino = ard.c_arduino()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.execTimer)
        self.lectura = ""

        
    def conectar(self):
        com = "COM"+self.txt_com.text()
        #print(com)
        # Inicializamos el arduino
        # Conexion a un puerto en LINUX /dev/tty
        # Enviar el COM que se ocupa en el dispositivo
        self.arduino.connect(com,self.btn_conectar)
        #self.txt_com.setText("")
        if(self.arduino.verifyConnection()):
            # Si esta conectado...           
            self.txt_com.setEnabled(False)
            self.txt_arduino.setEnabled(True)
            #self.txt_arduino.setFocus()            
            #self.beginRead()
            self.timer.start(10)
        else:
            self.timer.stop()

    def beginRead(self):
        if not self.timer.isActive():
            self.timer.start(10)
        else:
            self.timer.stop()

    def getLectura(self):
        if self.arduino.verifyConnection():
            return self.lectura
        else:
            return "Desconectado"

    # Timer para el Python
    def execTimer(self):
        if self.arduino.inWaiting():
            self.lectura = self.arduino.read()
            self.lectura = self.lectura.replace("\n", "")
            self.lectura = self.lectura.replace("\r", "")
            self.txt_arduino.setText(self.lectura);
            #print(self.lectura)

    def close(self):
        self.arduino.disconnect()
        if self.timer.isActive():
            self.timer.stop()

        


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyApp()
#     window.show()
#     sys.exit(app.exec_())
