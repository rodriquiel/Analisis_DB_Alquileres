# -*- coding: utf-8 -*-
"""DBconAlquileres.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11mFmGzNeyDFtUfyjpqgrL4CtrzN0gf4Z
"""

import pandas as pd

dataset = pd.read_csv('alquiler.csv', sep =';')

"""#Reporte de analisis 1"""

pd.set_option('display.max_rows',15) #Aumenta el maximo de filas que muestra el dataset al llamarlo, se puede aplicar a columnas

dataset

dataset.describe() #datos estadisticos basicos del dataset (mediana, cuartiles, desviacion estandar)

dataset.info() #Muestra info relacionada al dataset (cant. de no nulos, tipos de las columnas, etc)

dataset.head(11) #Muestra las primeras n lineas (5 por defecto)

"""##Info general sobre base de datos"""

dataset.dtypes

tiposDatos = pd.DataFrame(dataset.dtypes, columns = ['Tipos de datos'])
tiposDatos.columns.name = 'Variables'

tiposDatos #Muestra los datos con el formato especificado en la linea de codigo anterior

print('La base de datos presenta {} registros y {} variables'.format(dataset.shape[0], dataset.shape[1]))

"""##Eliminando datos repetidos y/o innecesarios

##Eliminar repetidos
"""

dataset['Tipo']

tipoInmueble = dataset['Tipo']
tipoInmueble.drop_duplicates(inplace = True) #Elimina datos repetidos

type(tipoInmueble)

"""##Organizacion de la visualizacion"""

tipoInmueble = pd.DataFrame(tipoInmueble)

tipoInmueble.index = range(tipoInmueble.shape[0])

tipoInmueble.columns.name = 'Indice'

tipoInmueble

#Ejemplo aparte
datos = {'A': {'X':1, 'Y':3}, 'B': {'X':2,'Y':4}}
df = pd.DataFrame(datos)
df

"""#Filtrado de datos

##Inmuebles Residenciales
"""

list(dataset['Tipo'].drop_duplicates()) #genera lista de tipos de inmuebles

residencial = ['Habitación',
 'Casa',
 'Departamento',
 'Casa en condominio',
 'Casa comercial',
 'Casa de villa'] #lista de inmuebles residenciales
residencial

seleccion = dataset['Tipo'].isin(residencial) #crea una series de booleans con true en caso de que la linea se encuentre en la lista que se paso como parametro
seleccion

data_res = dataset[seleccion] #genera un dataframe con los que cumplen la condicion aplicada en seleccion
data_res

data_res.shape[0]

data_res.index = range(data_res.shape[0]) #Modifica los indices y los coloca en forma ascendente, ya que antes contenian los indices del dataset
data_res

"""#Exportacion base de datos"""

data_res.to_csv('alquiler_residencial.csv', sep=';') #exporta con la columna de indices

data_res.to_csv('alquiler_residencial.csv', sep=';', index = False)

"""#Reporte de analisis: selecciones y frecuencias"""

dataset_res = pd.read_csv('alquiler_residencial.csv', sep = ';')
dataset_res.head(10)

"""##Seleccionar solamente inmuebles clasificados con tipo 'Departamento'"""

seleccion1 = dataset_res['Tipo'] == 'Departamento' #Series booleana con lineas segun cumplen el criterio (True)
seleccion1

n1 = dataset_res[seleccion1] #Muestra DF con filas que cumplen la condicion de seleccion1
n1

frec_n1 = n1.shape[0] #Frecuencia de la condicion dada en seleccion1
frec_n1

"""##Seleccionar inmuebles clasificados con tipos 'Casa', 'Casa en condominio' y 'Casa de villa'"""

seleccion2 = (dataset_res['Tipo'] == 'Casa') | (dataset_res['Tipo'] == 'Casa en condominio') | (dataset_res['Tipo'] == 'Casa de villa')
seleccion2

n2 = dataset_res[seleccion2]
frec_n2 = n2.shape[0]
frec_n2

"""##Seleccionar inmuebles con area entre 60 y 100 metros cuadrados (incluyendo limites)"""

seleccion3 = (dataset_res['Area'] >=60) & (dataset_res['Area'] <=100)
seleccion3

n3 = dataset_res[seleccion3]
frec_n3 = n3.shape[0]
frec_n3

"""##Seleccionar inmuebles que tengan por lo menos 4 cuartos y alquiler menor a $2.000,00"""

seleccion4 = (dataset_res['Cuartos'] >=4) & (dataset_res['Valor']<2000)
seleccion4

n4 = dataset_res[seleccion4]
frec_n4 = n4.shape[0]
frec_n4

print("Nº inmuebles clasificados con tipo 'Departamento' -> {}".format(frec_n1))
print("Nº inmuebles clasificados con tipo 'Casa', Casa en condominio' y 'Casa de villa' -> {}".format(frec_n2))
print("Nº inmuebles clasificados con area entre 60 y 100 metros cuadrados (incluyendo limites) -> {}".format(frec_n3))
print("Nº inmuebles clasificados que tengan por lo menos 4 cuartos y alquiler menor a $2.000,00 -> {}".format(frec_n4))

"""#Tratamiento de datos faltantes"""

dataset_res = pd.read_csv('alquiler_residencial.csv', sep = ';')
dataset_res.head(10)



"""##Recorrer DF para saber donde hay valores nulos"""

dataset_res.isnull() #tambien puede usarse .notnull()

dataset.info() #Informa cantidad de elementos y cantidad de no nulos por columna

dataset_res[dataset_res['Valor'].isnull()] #Devuelve DF con filas donde Valor es NaN

"""##Se opta por eliminar las lineas donde el casillero 'Valor' es nulo"""

numLineas = dataset_res.shape[0]
dataset_res.dropna(subset = ['Valor'], inplace = True) #Elimina nulos en 'Valor' y actualiza dataset_res
numLineasAct = dataset_res.shape[0]
numLineas - numLineasAct

dataset_res[dataset_res['Valor'].isnull()] #Muestra que ya no hay valores nulos en 'Valor

"""##Tratamiento Condicional

###Se propone eliminar departamentos en los cuales el valor de 'Mantenimiento' es **NaN**
"""

dataset_res[dataset_res['Mantenimiento'].isnull()].shape[0]

seleccionD = (dataset_res['Mantenimiento'].isnull()) & (dataset_res['Tipo']=='Departamento')

numLineas = dataset_res.shape[0]
dataset_res = dataset_res[~seleccionD] #Elimina filas de departamentos donde 'Mantenimiento' es nulo
numLineasAct = dataset_res.shape[0]
numLineas - numLineasAct

dataset_res[dataset_res['Mantenimiento'].isnull()].shape[0] #Lineas restantes con 'Mantenimiento' nulo

"""###Se propone rellenar los casilleros de mantenimiento e impuestos nulos restantes con ceros"""

dataset_res.fillna({'Mantenimiento':0, 'Impuesto':0}, inplace = True) #Reemplaza los valores nulos con ceros de las columnas correspondientes

dataset_res[dataset_res['Mantenimiento'].isnull()].shape[0] #Lineas restantes con 'Mantenimiento' nulo (cero)

"""##Exportacion Archivo actualizado"""

dataset_res.to_csv('alquiler_residencialSN.csv', sep=';', index = False)

"""#Creacion nuevas variables para analisis de la base de datos"""

datos_res = pd.read_csv('alquiler_residencialSN.csv', sep=';')

datos_res.head(10)

"""##Valor bruto"""

datos_res['Valor bruto'] = (datos_res['Valor']) + (datos_res['Mantenimiento']) + (datos_res['Impuesto'])
datos_res.head(10)

"""##Valor por metro cuadrado"""

datos_res['Valor por m2'] = (datos_res['Valor'])/(datos_res['Area'])
datos_res['Valor por m2'] = datos_res['Valor por m2'].round(2)
datos_res.head(10)

"""##Valor bruto por metro cuadrado"""

datos_res['Valor bruto por m2'] = ((datos_res['Valor bruto'])/(datos_res['Area'])).round(2)
datos_res.head(10)

"""##Se propone resumir los 'Tipos' a solo dos opciones: Casa o Departamento"""

casa = ['Casa','Casa en condominio','Casa de villa']

datos_res['Tipo agrupado'] = datos_res['Tipo'].apply(lambda x: 'Casa' if x in casa else 'Departamento') 
datos_res

"""##Exclusion variables innecesarias

###Se propone retirar la columna 'Impuesto' ya que la mayoria de los valores eran nulos que fueron reemplazados por cero
"""

datos_aux = pd.DataFrame(datos_res[['Tipo agrupado', 'Valor por m2', 'Valor bruto', 'Valor bruto por m2']])
datos_aux.head(10)

"""###Disitntas maneras de borrar una columna"""

del datos_aux['Valor bruto']
datos_aux.pop('Valor bruto por m2')
#datos_aux.drop(['Valor bruto', 'Valor bruto por m2'], axis = 1, inplace = true)
datos_aux.head(10)

datos_res.drop('Impuesto', axis = 1, inplace = True)
datos_res.head(10)

"""#Creacion agrupamientos para aplicar a estadistica descriptiva

##Se propone calcular la media para cada uno de los distritos que pertenecen al banco de datos
"""

datos_res.head(10)

datos_res['Valor'].mean() #Devuelve la media de todos los valores de la columna 'Valor' de la tabla

barrios = list(datos_res.Distrito.unique())
barrios

grupo_barrio = datos_res.groupby('Distrito')
grupo_barrio.groups #Muestra en un diccionario que indice le pertenece a cada barrio (llave)

for barrio, data in grupo_barrio:
  print(data) #Crea un dataframe para cada barrio

"""###Muestra media de cada barrio"""

for barrio, data in grupo_barrio:
  print('{} -> {}'.format(barrio, (data.Valor.mean()).round(2) ))

grupo_barrio['Valor'].mean().round(2) #Mismo resultado

grupo_barrio[['Valor', 'Mantenimiento']].mean().round(2) #Crea DF con las medias de 'Valor' y 'Mantenimiento'

"""##Otras estadisticas descriptivas"""

grupo_barrio['Valor'].describe().round(2) 
#cantidad de líneas, la media, la desviación estándar, los cuartiles y el valor máximo

"""###Al mirar minimos y maximos se observa una gran diferencia en algunos distritos, esto se debe a que la base se trata de alquileres pero se colaron algunos valores de ventas"""

grupo_barrio['Valor'].aggregate(['min', 'max']).rename(columns = {'min':'Minimo','max':'Maximo'})

"""##Importacion libreria matplot"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import matplotlib.pyplot as plt
plt.rc('figure', figsize = (20,10))

"""###En el siguiente grafico se observa las diferencias de las medias de los distintos distritos, lo que deja en evidencia el problema de los valores planteado anteriormente"""

fig = grupo_barrio['Valor'].mean().plot.bar(color = 'green')
fig.set_ylabel('Valor del alquiler')
fig.set_title('Valor medio del alquiler por distrito', {'fontsize':22})

"""###En este grafico se observa la gran diferencia en los maximos"""

fig2 = grupo_barrio['Valor'].max().plot.bar(color = 'blue')
fig2.set_ylabel('Valor del alquiler')
fig2.set_title('Valor maximo del alquiler por distrito', {'fontsize':22})

"""#Exclusion outliers (puntos fuera de la curva)

##Grafico Box-Plot: muestra donde se concentran los datos y los outliers
"""

datos_res.boxplot(['Valor'])

valor = datos_res['Valor']

Q1 = valor.quantile(0.25)
Q3 = valor.quantile(0.75)
IIQ = Q3 - Q1 #Intervalo intercuartil
lim_inf = Q1 - 1.5*IIQ
lim_sup = Q3 + 1.5*IIQ

seleccion = (valor >= lim_inf) & (valor <= lim_sup)

"""###Se eliminan los outliers gigantes a traves del uso de los limites del boxplot y se genera un nuevo boxplot con los datos filtrados"""

datos_new = datos_res[seleccion]

datos_new.boxplot(['Valor'])

"""##Comparacion histogramas con y sin outliers

###Con outliers
"""

datos_res.hist(['Valor'])

"""###Sin outliers"""

datos_new.hist(['Valor']) #Eje y marca frecuencia y eje x valor

"""#Excluyendo outliers por grupo

##Se realiza el mismo trabajo solo que esta vez teniendo en cuenta el 'Tipo' al que pertenece cada valor analizado
"""

datos_res.boxplot(['Valor'], by = ['Tipo'] )

datos_res.hist(['Valor'], by = ['Tipo'])

grupo_tipo = datos_res.groupby('Tipo')['Valor']

"""###Se generan cuartiles y limites para cada tipo a partir de grupo_tipo"""

Q1 = grupo_tipo.quantile(0.25)
Q3 = grupo_tipo.quantile(0.75)
IIQ = Q3 - Q1 #Intervalo intercuartil
lim_inf = Q1 - 1.5*IIQ
lim_sup = Q3 + 1.5*IIQ

lim_sup

lim_inf

datos_new = pd.DataFrame()
for tipo in grupo_tipo.groups.keys():
  eh_tipo = datos_res['Tipo'] == tipo
  eh_limites = (datos_res['Valor'] >= lim_inf[tipo]) & (datos_res['Valor'] <= lim_sup[tipo])
  seleccion = eh_tipo & eh_limites
  datos_seleccion = datos_res[seleccion]
  datos_new = pd.concat([datos_new,datos_seleccion])

"""###Se observa en los resultados los distintos boxplot e histogramas separados por tipos y corregidos luego de la exclusion de los outliers"""

datos_new.boxplot(['Valor'], by = ['Tipo'])

datos_new.hist(['Valor'], by = ['Tipo'])

datos_new.to_csv('alquiler_residencial_sin_outliers.csv', sep=';', index = False)

"""#Graficos finales"""

datos_final = pd.read_csv('alquiler_residencial_sin_outliers.csv', sep = ';')
datos_final.head(10)

area = plt.figure() #Area para graficar

"""###Configuracion posiciones graficos"""

g1 = area.add_subplot(2,2,1) #lineas, columnas, posicion
g2 = area.add_subplot(2,2,2)
g3 = area.add_subplot(2,2,3)
g4 = area.add_subplot(2,2,4)

"""##Creacion graficos"""

from tables import group
#Garfico de dispersion
g1.scatter(datos_final.Valor, datos_final.Area)
g1.set_title('Garfico de dispersion de valor por Area')

#Histograma
g2.hist(datos_final.Valor)
g2.set_title('Histograma Valor')

#Grafico de lineas con muestra aleatoria
datos_g3 = datos_final.Valor.sample(100)
datos_g3.index = range(datos_g3.shape[0])
g3.plot(datos_g3)
g3.set_title('Grafico de valor con muestra aleatoria')

#Grafico de barras
grupo = datos_final.groupby('Tipo')['Valor']
label = grupo.mean().index
valores = grupo.mean().values
g4.bar(label, valores)
g4.set_title('Grafico de barras de valor medio por tipo')

"""##Muestra graficos"""

area

area.savefig('graficos.png', dpi = 300, bbox_inches = 'tight')