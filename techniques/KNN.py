from techniques.Medidas_Similitud import Euclidiana,Euclidiana_norm,Manhattan,Jaccard,Coseno,Sorence_Dice,Canberra
from statistics import multimode


metricas = [Manhattan,Euclidiana,Euclidiana_norm,Jaccard,Coseno,Sorence_Dice, Canberra]

def KNN(test,training):
    ###DEFINIR EL VALOR DE "K"  - Un número entre 1 y el total de registros de la instancia (entrenamiento)
    
    met = 6 #Canberra
    K = 5

    if met==3 or met==4 or met==5:
        rev = True
    else:
        rev = False 

    instancia = training
    prueba = test

    #print("Total de datos de la Instancia",len(prueba))

    contAciertos = 0 

    for registroNC in prueba: #para recorrer a todos los registros de prueba y aplicar al algoritmo K-NN
        #print("Clasificación del registro: ")
        #print(registroNC) #registor de prueba procesado para su clasificacion

        NC = registroNC[0] #vector de caracteristicas del registro actual de prueba

        estructuraDatos = {} #inicializacion de la estructura de datos

        for NoCaso, i in enumerate(instancia):
            distancia_NC_i = metricas[met](NC, i[0])
            #print(distancia_NC_i)
            estructuraDatos[NoCaso] = distancia_NC_i

        #print(estructuraDatos)  # La distancia de los registros con el registroNC

        ordenado = sorted(estructuraDatos.items(), key=lambda x: x[1],reverse=rev) #ordena los registros
        #de menor a mayor de acuerdo con la distancia con el registroNC
        #print(ordenado)

        temporalK = []
        for i in range(K):
            NoCaso = ordenado[i][0]
            #print(etiqueta)
            registro = instancia[NoCaso]
            #print(registro)
            temporalK.append(registro[1]) #obtencion de la etiqueta

        print("Clases de los vectores más cercanos al registro NC:")
        print(temporalK)  #los primeros K vectores
        
  
        moda = multimode(temporalK)
        respKnn = moda[0]  # si existe más de una moda se queda con la primera de ellas  

        print("Clase asignada por el KNN: "  + str(respKnn))
        #print("Clase Real: " + str(registroNC[1]))

        # if str(respKnn) == str(registroNC[1]):
        #     contAciertos += 1


    #rend = contAciertos/len(prueba)*100
    # print("\nK = ",K)
    # print("Total de aciertos: " + str(contAciertos))
    # print("Total de pruebas: " + str(len(prueba)))
    # print("Rendimiento: " + str(rend))

    #data = [K,rend,contAciertos]

    #for el in ordenado:
    #W    print(el)

    #return data


#Practica:
#Realizar la aplicación de KNN para el calculo del rendimiento de la técnica utilizando la instancia WINE
#   Consideraciones:
#           *Añadir el código necesario para realizar la busqueda automatizada del valor de K que de mejores resultados
#           *Reportar que valor de K es el mejor y que rendimiento genera
#           *PROBAR OTRAS METRICAS DE SIMILITUD
#           *Generar matriz de confusión

