import sys
import json
from PyQt5 import uic, QtWidgets, QtCore
import pandas as pd
# Modulo/clase arduino
import arduinoWind as ard

from techniques.knn_2 import knn 
from techniques.asociador_lineal import asociador_lineal as asolin
from techniques.naive_bayes import naive_bayes as naibay
import techniques.mapeador as mapea

from numpy import interp

qtCreatorFile = "main.ui" # Nombre del archivo .ui aqui.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Área de los Signals y Configuraciones Iniciales
        self.btnArduino.clicked.connect(self.conectar)
        
        self.tecnicas = self.read_yeison() 
        self.key = 0         
           
        self.tecnica = list(self.tecnicas.items())[0][0]   
        self.funcion = self.tecnicas[self.tecnica]
        
        # New Window
        self.ardApp  = QtWidgets.QApplication(sys.argv)
        self.ardWindow = ard.MyApp()
       
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.execTimer)
        self.timer.start(10)
        self.dataset = mapea.leer_dataset("instance/zoo.csv",delimitador="\t")
        self.puntero = -1
        self.dickJSON, self.keys = self.read_yeison2()
        self.lectAnterior = ""
        self.mapeoRango = 2
        self.vp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    def siguiente(self):
        self.puntero += 1

        if(self.puntero > len(self.keys)-1):  
            self.puntero = -1
            self.vp[self.puntero] = int(self.txtRespuesta.text())-1 #Esta no le entendi xd  el vp[ puntero ] = valor
            print(self.vp)
            knn(self.vp, self.dataset)
            print(self.vp)
            #self.identificar()
            return
        self.vp[self.puntero-1] = int(self.txtRespuesta.text())-1

        key = self.keys[self.puntero]
        pregunta = self.dickJSON[key]["Question"]
        respuesta = self.dickJSON[key]["TAnswer"]
        self.mapeoRango = len(respuesta)
        self.lblPregunta.setText(key+"."+pregunta)

        r = ""
        for el in respuesta:
            r += str(el) 
            r += " "

        self.lblRespuesta.setText(r)
        print(respuesta)
        


    def anterior(self):
        self.puntero -= 1

        if(self.puntero < 0):   
            self.puntero = -1
            return
        
        key = self.keys[self.puntero]
        pregunta = self.dickJSON[key]["Question"]
        respuesta = self.dickJSON[key]["TAnswer"]
        self.mapeoRango = len(respuesta)
        
        self.lblPregunta.setText(key+"."+pregunta)

        r = ""
        for el in respuesta:
            r += str(el) 
            r += " "

        self.lblRespuesta.setText(r)
        print(respuesta)
       
    def read_yeison2(self):
        nombreJSON = 'questions.json'
        file = open(nombreJSON, 'r')
        data = json.load(file)
        file.close()          
        
        keys = list(data.keys())     
        return data, keys


    def read_yeison(self):
        nombreJSON = 'config.json'
        file = open(nombreJSON, 'r')
        data = json.load(file)
        file.close()
        tecnicas = data['tecnicas']
        return tecnicas

    def mapearResp(self,valor,rango):
        #O-1023
        resp = round(interp(valor,[0,1023],[1,rango]))
        return resp


    def conectar(self):
        self.ardWindow.show()
    

    def setInstancia(self):                
        self.key = self.cbInstancia.currentIndex()
        self.instancia = self.instancias[self.keyInst[self.key]] 

        archivo, delim, head, index = list(self.instancia.values())       
        self.dfDataset = mapea.leer_dataset(archivo, delim, eval(head), eval(index))      
        self.dfDsMap, self.discretizador = mapea.mapear_dataset(self.dfDataset) 
        print(self.dfDataset, "\n") 

        
    def setTecnica(self):        
        index = self.cbTecnica.currentIndex()
        self.tecnica = str(self.cbTecnica.itemText(index))
        self.funcion = self.tecnicas[self.tecnica]


    def identificar(self):
        self.puntero = -1
        print("\n----- {} -----".format(self.tecnica))
        text = (self.instancia_ard.text())
        #vp = list(map(int, text.split(',')))            
        vpMap = self.mapearVP(vp)
        func = "{}({},{})".format(
            "eval(self.funcion)", "vpMap", "self.dfDsMap")             
        decision = eval(func)
        lon = len(self.discretizador) - 1
        decisionKey = mapea.get_key(self.discretizador[lon], decision)
        print("Decision: ", decisionKey)
        print()
        

    def mapearVP(self, vpArduino):
        #print("\nvp INO:      ",vpArduino)
        mins = self.dfDataset.min().to_list()
        maxs = self.dfDataset.max().to_list()
        
        vp = list(map(lambda x, y, z: round(x*(z-y)/1023+y, 4), vpArduino, mins, maxs ))
        #print("vp INO map:  ",vp)
        
        
        dtipos = self.dfDataset.dtypes
        vpMap = mapea.discretizar_vp(vp, self.discretizador, dtipos)
        #print("vp mapeado:  ",vpMap)
        #print()       
        
        return vpMap


    # Timer para el Python
    def execTimer(self):
        lect = self.ardWindow.getLectura()
        
        if(lect == "Desconectado"):
            self.lblArdState.setText(lect)
            return
        elif lect != self.lectAnterior:
            self.lectAnterior = lect
            lect = lect.split(" ")
            if len(lect) >= 3:
                self.lblArdState.setText(lect[0])    
                self.respMapeada = self.mapearResp(int(lect[0]),self.mapeoRango)
                self.txtRespuesta.setText(str(self.respMapeada))    
                if(lect[2] == "1"):
                    self.siguiente()
                    
                elif(lect[1] == "1"):
                    self.anterior()


    def listToStr(self, lista):
        listaString = str(lista)
        lon = len(listaString)
        cadena = str(listaString[1: lon-1])
        return cadena


    def closeEvent(self, event):
        self.ardWindow.close()
        if self.timer.isActive():
            self.timer.stop()
        sys.exit(self.ardApp.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
