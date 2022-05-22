#Metricas Similitud Zubiri Valdez Hedson Leonardo
# X = Vector Problema VP
# Y = Vectores a someter a prueba


from dis import dis
from math import sqrt

X = [4,3,4,2,1]
Y = [[5,2,7,5,1],[3,4,5,2,4],[3,8,6,9,3]]

RESP = []

def Manhattan(X,Y):
    dist=0
    for i in range(len(X)):
        dist += abs(X[i]-Y[i])

    return dist


def Canberra(X,Y):
    dist=0
    for i in range(len(X)):
        opArr = abs(X[i] - Y[i])
        opAba = abs(X[i]) + abs(Y[i])
        dist += opArr/opAba

    return dist


#Manhattan(X, Y)

#Euclidiana(X,Y)
def Euclidiana(A, B):
    distancia = 0
    for i in range(len(A)):
        distancia += (A[i]-B[i])**2
    distancia = distancia ** (1/2)
    distancia = round(distancia, 2)
    return distancia

def Euclidiana_norm(X,Y):
    dist=0
    for i in range(len(X)):
        dist += X[i]**2 - 2*(X[i]*Y[i]) + Y[i]**2
    return dist
    

#Euclidiana_norm(X,Y)


def Sorence_Dice(X,Y):
    opArr = 0
    opAba = 0
    for i in range(len(X)):
        opArr += X[i]*Y[i]
        opAba += X[i]**2 + Y[i]**2
    
    dist = 2*opArr / opAba
    return dist
        

#Sorence_Dice(X,Y)

def Coseno(X,Y):
    opArr = 0
    xAba = 0
    yAba = 0
    for i in range(len(X)):
        opArr += X[i]*Y[i]
        xAba += X[i]**2
        yAba += Y[i]**2
    
    dist = opArr / sqrt(xAba*yAba)
    return dist

#Coseno(X,Y)


def Jaccard(X,Y):
    opArr = 0
    opAba = 0
    for i in range(len(X)):
        opArr += X[i]*Y[i]
        opAba += X[i]**2 + Y[i]**2 - X[i] * Y[i]
    
    dist = opArr / opAba
    return dist


#Jaccard(X,Y)