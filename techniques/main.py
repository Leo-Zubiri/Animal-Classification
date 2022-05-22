import mapeador
from asociador_lineal import asociador_lineal as al
from naive_bayes import naive_bayes as nb

# archivo = "instances/prueba_nb_Y.txt"
# vp = ["Soleado", "Frío", "Alta", "Fuerte"]
# dfArchivo = mapeador.leer_dataset(archivo, delimitador="\t")

archivo = "instances/Instancia_iris.csv"
vp = [5.7, 3.2, 3, 1.7]

# archivo = "instances/Instancia_clase.csv"
# vp = [56, 78, 90, 71, 47, 68]

# archivo = "instances/Instancia_cancer.csv"
# vp = [3, 2, 3, 1, 1, 2, 3, 1, 5]

# archivo = "instances/Instancia_wine.csv"
# vp = [12, 1, 2.5, 22, 110, 3.1, 3, 0.32, 1.18, 7.69, 0.50, 2.22, 623]


# # Descomentar siguiente linea para todos los casos menos prueba nb
dfArchivo = mapeador.leer_dataset(archivo) 

# print(dfArchivo)
dfArchivoD, discretizador = mapeador.mapear_dataset(dfArchivo)
#print(dfArchivoD)

#mapeador.crear_archivo(dfArchivoD, "", "iris_discretizada")

dtipos = dfArchivo.dtypes
vpDisc = mapeador.discretizar_vp(vp, discretizador, dtipos)

# decision = al(vpDisc, dfArchivoD)
decision = nb(vpDisc, dfArchivoD)

# dec = mapeador.get_key(discretizador[len(discretizador)-1], decision)
print("VP: ", vp)
print("Decision: ", decision)
