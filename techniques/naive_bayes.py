import pandas as pd
#import mapeador as lsd
import techniques.mapeador as lsd
import copy

def naive_bayes(vectorP, dfDataset):  
    #print("\n----- Naive Bayes -----")
    totalCasos = len(dfDataset)
    vector_conj, vector_dic = [], []

    # ! ----------------------------------------------------------------------------------
    # Obtenemos los vectores de conjuntos y diccionarios    
    for i in dfDataset:
        conjunto = set(dfDataset[i].to_list())        
        vector_conj.append(conjunto)
        
        diccionario = {key:info for info, key in enumerate(conjunto)}
        vector_dic.append(diccionario)

    # print()
    # print(vector_dic[-1])
    # for i in vector_dic:
    #     print(i)
    # print()

    # ! ----------------------------------------------------------------------------------

    # Vector contador de decisiones de cada atributo
    contDecisiones = []
    # Vector con las decisiones
    decisiones = [0 for i in range(len(vector_conj[-1]))]

    # Llenamos el vector 'contDecisiones' con ceros y sus correspondientes vectores
    for i in vector_conj:    
        aux = []
        for j in i:
            aux.append(decisiones.copy())
        
        contDecisiones.append(aux)

    contDecisiones.pop() # Eliminamos las decisiones

#    print(contDecisiones)

    # Contamos todas las decisiones    
    for i in range(dfDataset.shape[0]):    
        k = vector_dic[-1][dfDataset.iloc[i, -1]]
        respuesta = k
        decisiones[respuesta] += 1
        for j in range(dfDataset.shape[1]-1):
            k = vector_dic[j][dfDataset.iloc[i, j]]
            contDecisiones[j][k][respuesta] += 1

    # print("-"*10, "Decisiones contadas", "-"*10)
    # for i in contDecisiones:
    #     print(i)
    # print()


    # ! -----------------------------------------------------------------------------------
    # Creamos una copia de las decisiones para obtener las probabilidades
    # (Solo nos importa copiar la estructura)
    # (podemos sobreescribir "contDecisiones")
    probabilidades = copy.deepcopy(contDecisiones)
    probDecision = [round(i/totalCasos,4) for i in decisiones]

    for i in range(len(probabilidades)):
        for j in range(len(probabilidades[i])):
            for k in range(len(decisiones)):
                probabilidades[i][j][k] = round(contDecisiones[i][j][k]/decisiones[k], 4)

    # print("-"*10,"Probabilidades","-"*10)
    # for i in probabilidades:
    #     print(i)
    # print()

    # print("-"*10,"Decisiones y su probabilidad","-"*10)
    # print(decisiones)
    # print(probDecision)
    # print()

    # ! ----------------------------------------------------------------------------------
    # Resolvemos ahora el caso
    # Llenamos de 1 para luego ser multiplicadas por las probabilidades obtenidas
    probCaso = [1 for i in decisiones]
    for k in range(len(probCaso)):
        probCaso[k] *= probDecision[k]
        for i in range(len(vectorP)):
            # Obtenemos el indice del caso dentro de nuestro vector diccionario
            j = vector_dic[i].get(vectorP[i])
            if(j == None):                              
                continue
            
            probCaso[k] *= probabilidades[i][j][k]
        probCaso[k] = round(probCaso[k], 4)

    decisionCaso = -1
    auxProb = -1
    # Buscamos la mayor decision
    for i in range(len(probCaso)):
        if(probCaso[i] > auxProb):
            auxProb = probCaso[i]
            decisionCaso = i

    # print("-"*10,"Resolucion del caso","-"*10)
    print("Caso: ", vectorP)
    # print("                  ", vector_conj[-1])
    # print("Prob de Decision: ", probCaso)
    # decisionClase = list(vector_dic[-1].keys())[decisionCaso]

    decisionClase = list(vector_dic[-1].keys())[decisionCaso]    

    print("Clase:  ", decisionClase)    
    return decisionClase

