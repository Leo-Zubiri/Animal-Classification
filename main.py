from ast import While
import sys
import json
from PyQt5 import uic, QtWidgets, QtCore, QtGui, QtNetwork
import pandas as pd
# Modulo/clase arduino
import arduinoWind as ard
from serpapi import GoogleSearch
import random as rnd
from random import randint
import requests

from techniques.knn_2 import knn 
from techniques.asociador_lineal import asociador_lineal as asolin
from techniques.naive_bayes import naive_bayes as naibay
import techniques.mapeador as mapea

from numpy import interp
from PyQt5.QtWidgets import QMessageBox,QLabel


# dale run, ya esta importado QtWidgets, dale run, comenta la importacion, si no jala, entonces hay que 
qtCreatorFile = "main.ui" # Nombre del archivo .ui aqui.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Área de los Signals y Configuraciones Iniciales
        self.btnArduino.clicked.connect(self.conectar)
        self.params = json.load(open('serpapi_config.json', 'r'))["params"]
        self.pointer = 0
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
        self.imgs = []
        self.manager = None

        self.animales = []
        self.params = json.load(open('serpapi_config.json', 'r'))["params"]

    def siguiente(self):
        self.puntero += 1

        if(self.puntero > len(self.keys)-1):  
            self.puntero = -1
            self.vp[self.puntero] = int(self.txtRespuesta.text())-1 #Esta no le entendi xd  el vp[ puntero ] = valor
            print(self.vp)
            r = knn(self.vp, self.dataset)
             
            self.MessageResult(r)
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
    

     
    def setTecnica(self):        
        index = self.cbTecnica.currentIndex()
        self.tecnica = str(self.cbTecnica.itemText(index))
        self.funcion = self.tecnicas[self.tecnica]
        

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

    def MessageResult(self,r):
        #image1 image2 image3  QLabels       
        
        self.pointer = 0
        for i in range(3):      
            self.animales.append(r[1][i])    
        self.setimageAlt()

        res = "VP: {} \nClase: {} ".format(r[0],r[1])
        ret = QMessageBox.question(self, 'Resultados', res, QMessageBox.Ok)

        

        if ret == QMessageBox.Ok:
            self.imgs = []
            self.puntero = -1
            self.lblPregunta.setText("CONECTE EL ARDUINO Y PRESIONE UN BOTON PARA EMPEZAR")
            self.lblRespuesta.setText("....")
        self.animales = []

    def setimageAlt(self):
        try:

            for i in range(3):
                url = self.getURL("Animal "+self.animales[i])
                image = QtGui.QImage()
                image.loadFromData(requests.get(url).content)
                exec("self.image{}.setPixmap(QtGui.QPixmap(image))".format(i+1))

        except Exception as e:
            print(e)

    def getURL(self, buscar):
        self.params["q"] = buscar
        print(self.params)
        search = GoogleSearch(self.params)
        results = search.get_dict()
        url = results["images_results"][randint(0, 25)]["thumbnail"]
        return url


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
