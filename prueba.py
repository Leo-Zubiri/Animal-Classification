import techniques.mapeador as mapea
import json
import pandas as pd
from techniques.knn_2 import knn as knn
from techniques.asociador_lineal import asociador_lineal as asolin
from techniques.naive_bayes import naive_bayes as naibay

vp = [1,0,0,1,0,0,1,1,1,1,0,0,4,0,0,0,0] # OSO / BEAR

# vp = [0,1,1,0,1,1,0,0,1,1,0,0,2,1,0,0,2] # DUCK

#vp = [1,0,0,1,0,0,0,1,1,1,0,0,4,1,1,1,1] # GOAT
#vp = [1,0,0,1,0,0,0,1,1,1,0,0,4,1,0,1,1] # ELEPHANT
#vp = [1,0,0,1,0,0,1,1,1,1,0,0,2,0,1,1,1] #GIRL

# dataset = mapea.leer_dataset("instance/zoo.data") #DALE
dataset = mapea.leer_dataset("instance/zoo.csv",delimitador="\t")

# decisiones = naibay(vp, dataset)
# for i in decisiones:
#     print(dataset.iloc[i, -1]) #Dale ;) ;) ;) JAJAJA

knn(vp,dataset)
