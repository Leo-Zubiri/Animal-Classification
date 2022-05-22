import pandas as pd
import numpy as np
#import mapeador as lsd
import techniques.mapeador as lsd

def asociador_lineal(vectorP, dfDataset):#, archivo, delimitador=',', hasHeader=None, hasIndex=None, mapear=True):
    """
        vectorP (list): Vector con los 'N' datos requeridos por la instancia elegida.
        dfDataset (pandas.DataFrame): Dataset del archivo elegido.
    """
    # Leemos los datos
    # Usando la nueva funcion del archivo "leer_dataset.py"    
    #dfDataset = lsd.mapear_dataset(archivo, delimitador, hasHeader, hasIndex, mapear)
    #print("\n----- Asociador Lineal -----")
    datos, clases, clasesSet = [], [], set()

    # Separamos los datos de las clases
    for i in range(len(dfDataset)):
        datos.append(list(dfDataset.iloc[i])[:-1])    
        clases.append(dfDataset.iloc[i,-1])
        clasesSet.add(dfDataset.iloc[i, -1])
        #print(datos[i])

    # Identificamos las clases
    clasesDic = {}
    for i, j in enumerate(clasesSet):
        clasesDic[j] = i

    # Ciframos los clases
    clasesCifradas = []
    for i in range(len(clases)):
        a = []
        for j in range(len(clasesSet)):
            a.append(0)
        a[clasesDic[clases[i]]] = 1
        clasesCifradas.append(a)
        # print(datos[i], clasesCifradas[i], get_key(clasesDic, clasesDic[clases[i]]))

    
    # Operaciones de matrices con los datos y clases cifrados
    # con ayuda de numpy
    X = np.array(datos)
    Y = np.array(clasesCifradas).T
    Xt = X.T

    Paso1 = Xt.dot(X)
    Paso2 = np.linalg.inv(Paso1)
    Xpseudo = X.dot(Paso2)

    W = Y.dot(Xpseudo)

    vectorClase = W.dot(vectorP)
    
    indiceClase = list(vectorClase).index(max(vectorClase))
    decisionClase = lsd.get_key(clasesDic, indiceClase)    
    print("Caso: ",vectorP)
    print("Clase: ",decisionClase)        
    
    return(decisionClase)
    

# vectorP = [56, 78, 90, 71, 47, 68]
# archivo = "instances/Instancia_clase.csv"

#vectorP = [3, 2, 3, 1, 1, 2, 3, 1, 5]
#archivo = "instances/Instancia_cancer.csv"

# vectorP = [5, 3, 5, 0.3]
# archivo = "instances\Instancia_iris.csv"
# #archivo = "../instances/Instancia_iris.csv"

# # vectorP = [12, 1, 2.5, 22, 110, 3.1, 3, 0.32, 1.18, 7.69, 0.50, 2.22, 623]
# # archivo = "instances\Instancia_wine.csv"

# asociador_lineal(vectorP, archivo)
