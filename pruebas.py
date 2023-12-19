#Ejemplos de lectura de archivos

"""
with open('data/movimientos.csv', 'r') as resultado: 
    leer = resultado.read()
    print(leer)

##########################################################

resultado = open('data/movimientos.csv', 'r')
lectura = resultado.readlines()
print(lectura)
"""

##########################################################

import csv

midato = []

mifichero = open('data/movimientos.csv', 'r')
lectura = csv.reader(mifichero, delimiter=',', quotechar='"')
for items in lectura:
    #print(items)
    midato.append(items)

print("Mi lista: ", midato[0][1])