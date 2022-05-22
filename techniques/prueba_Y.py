import pandas as pd

#archivo = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data"

archivo = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

dfArchivo = pd.read_csv(archivo)#, header=None) 

# print(len(dfArchivo.iloc[0]))

print(dfArchivo.shape[1])
print(len(dfArchivo))

for i in range(len(dfArchivo)):

#     #print(dfArchivo.iloc[i, -1])
#     print(len(dfArchivo.iloc[i])-1)
    print(set(dfArchivo.iloc[i].to_list()))

# print(dfArchivo, "\n")  

# tipos = dfArchivo.dtypes 
# for i, head in enumerate(tipos.index):
#     columna = dfArchivo[head].to_list() 
#     print("{}\n\n{}\n\n{}\n\n".format(i,columna, dfArchivo[head]))
    