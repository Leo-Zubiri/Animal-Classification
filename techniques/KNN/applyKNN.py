
from KNN import KNN
from statistics import multimode

nomMets = ["Manhattan","Euclidiana","Euclidiana_norm","Jaccard","Coseno","Sorence_Dice","Canberra"]
testFiles = ["wine_test60.0.csv","wine_test70.0.csv","wine_test80.0.csv","wine_test90.0.csv"]
trainingFiles = ["wine_training60.0.csv","wine_training70.0.csv","wine_training80.0.csv","wine_training90.0.csv"]

#metricas = [0,1,2,3,4,5]  #aplicar metrica 0,1
metricas = [-1]
nfiles = [3] # aplicar KNN a los archivos 0,1,2

bestResults = []

with open("resultados.csv", "w") as f:
    lista=["        K"," Rendimiento"," Aciertos"]
    for el in lista:
        f.write('{},'.format(el))
    f.write("\n")

for archivo in nfiles:
    testFile = open(testFiles[archivo])
    trainingFile = open(trainingFiles[archivo])

    testContent = testFile.readlines()
    trainContent = trainingFile.readlines()

    lista = [linea.split(",") for linea in testContent]
    test = [ [ list(map(float,x[:len(lista[0])-1])), int(x[len(lista[0])-1].replace("\n","")) ] for x in lista ]

    lista = [linea.split(",") for linea in trainContent]
    training = [ [ list(map(float,x[:len(lista[0])-1])), int(x[len(lista[0])-1].replace("\n","")) ] for x in lista ]

    print("Total de pruebas: ",len(testContent))

    for metrica in metricas:
        print('\n**** Metrica: {} Archivo: {} *****,'.format(nomMets[metrica],testFiles[archivo]))
        with open("resultados.csv", "a") as f:
            f.write('**** Metrica: {} Archivo: {} *****,'.format(nomMets[metrica],testFiles[archivo]))
            f.write("\n")
        resultados = []
        for k in range(1,len(testContent)+1,1):
            data = KNN(k,test,training,metrica)
            resultados.append(data)
            with open("resultados.csv", "a") as f:
                for el in data:
                    f.write('{},'.format(el))
                f.write("\n")

        #[[K,RENDIMIENTO,ACIERTOS],[...]]
        mayRend = max(resultados, key= lambda x: resultados[1])
        for el in resultados:
            if mayRend[1] == el[1]:
                bestResults.append(el)

print("\n",bestResults)
nK = [x[0] for x in bestResults]
print("K's: ",nK)

nK.sort()
print("\nK's orden: ",nK)
moda = multimode(nK)

print("\n K con mayor rendimiento en pruebas:",moda)
