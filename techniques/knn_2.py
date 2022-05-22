import pandas as pd
from statistics import multimode
from techniques.Medidas_Similitud import Canberra
from techniques.mapeador import separar_cc
# from Medidas_Similitud import Canberra
# from mapeador import separar_cc

def knn(vectorP, dfDataset):
    K = 3
    dataset = separar_cc(dfDataset)

    res = []
    for d in dataset:
        dist = Canberra(vectorP, d[0])
        res.append([d[1], dist])    

    resSorted = sorted(res, key=lambda x:x[-1])[:K]
    decisiones = [i[0] for i in resSorted]
    decisionClase = multimode(decisiones)[0]

    print("Caso: ",vectorP)
    print("Clase: ",decisionClase)     

    return(decisionClase)

