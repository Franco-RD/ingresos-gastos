#Ejemplos de lectura de archivos

"""
with open('data/movimientos.csv', 'r') as resultado: 
    leer = resultado.read()
    print(leer)

##########################################################

resultado = open('data/movimientos.csv', 'r')
lectura = resultado.readlines()
print(lectura)


##########################################################

import csv

midato = []

mifichero = open('data/movimientos.csv', 'r')
lectura = csv.reader(mifichero, delimiter=',', quotechar='"')
for items in lectura:
    #print(items)
    midato.append(items)

print("Mi lista: ", midato[0][1])

"""

##########################################################
# Ejemplo para registrar datos en csv
import csv 

mifichero = open('data/movimientos.csv', 'a', newline = '') #El newline es para que lo nuevo que agreguemos al archivo lo ponga en una nueva linea al final. Sino lo pondria al final de la ultima que ya existe
lectura = csv.writer(mifichero, delimiter=',', quotechar='"')
lectura.writerow(['24/04/2024', 'roscon de reyes', '-40'])

mifichero.close()  #Sino el archivo queda abierto