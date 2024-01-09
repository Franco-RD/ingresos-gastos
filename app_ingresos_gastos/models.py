from app_ingresos_gastos import MOVIMIENTOS_FILE, LAST_ID_FILE
import csv

def select_all():  #devolver una lista con todos los registros del fichero MOVIMIENTOS_FILE
    datos = []
    fichero = open(MOVIMIENTOS_FILE, 'r') #llamada al archivo csv
    csvReader = csv.reader(fichero, delimiter=',', quotechar='"') #accediendo a cada registro del archivo
    for items in csvReader:
        datos.append(items)  #Recorremos el archivo y agregamos cada linea a la lista datos
    fichero.close()

    return datos


def select_by(id, condicion):  #devolver un registro segun el id dado o vacio si no lo encuentra en MOVIMIENTOS_FILE
    miFicheroDelete = open(MOVIMIENTOS_FILE, 'r')
    lecturaDelete = csv.reader(miFicheroDelete, delimiter=',', quotechar='"')
    registro_buscado = []

    for item in lecturaDelete:
        if condicion == "==":
            if item[0] == str(id):                 
                #registro_buscado.append(item)
                registro_buscado = item  #En vez de hacer un append, se iguala el array que devolvemos a item, para que no quede un array de arrays. Asi en delete.html, podemos recorrer con un solo subindice en lugar de dos. 
        
        elif condicion == "!=":
            if item[0] != str(id):  #Filtro toda la base de datos y la vuelvo a guardar sin el id que quiero borrar
                registro_buscado.append(item)   
        
        elif condicion == "dic":                       
            if item[0] == str(id):  #Encuentro el id buscado para actualizar 
                registro_buscado = dict()    
                registro_buscado['id'] = item[0]
                registro_buscado['fecha'] = item[1]
                registro_buscado['concepto'] = item[2]
                registro_buscado['monto'] = item[3]    
    
    miFicheroDelete.close()
        
    return registro_buscado


def delete_by(id, registros):  #borrar un registro segun el id dado en MOVIMIENTOS_FILE
    fichero_guardar = open(MOVIMIENTOS_FILE, 'w', newline = '')  #El parametro newline es para que vaya haciendo un salto de linea con cada escritura
    csv_writer = csv.writer(fichero_guardar, delimiter=',', quotechar='"')  #Escribir con metodo writer
    for datos in registros:
        csv_writer.writerow(datos)  
    
    fichero_guardar.close()


def insert(requestForm):  #agregar un registro nuevo con un id unico y acumulativo a MOVIMIENTOS_FILE
    ################## Generar el ultimo ID para la base de datos ##########################
    lista_id = []
    last_id = "0"
    new_id = 0

    ficheroId = open(LAST_ID_FILE, 'r') 
    csvReaderId = csv.reader(ficheroId, delimiter=',', quotechar='"') 
    for items in csvReaderId:
        lista_id.append(items[0])  
    ficheroId.close()
    
    last_id = lista_id[-1]
    new_id = int(last_id) + 1

    ################## Guarda el ultimo ID generado en last_id #############################

    fichero_new_id = open(LAST_ID_FILE, 'w')  #El metodo w para abrir pisa lo ultimo para guardar lo nuevo
    fichero_new_id.write(str(new_id))
    fichero_new_id.close()

    ########################################################################################

    mifichero = open(MOVIMIENTOS_FILE, 'a', newline = '')  #Acceder al archivo y configurar para cargarle registros 
    escritura = csv.writer(mifichero, delimiter=',', quotechar='"')  #Escribir con metodo writer
    escritura.writerow([new_id, requestForm['fecha'], requestForm['concepto'], requestForm['monto']])  #request.form es un array de tuplas con todos los datos que cargamos en el formulario. Cada clave de cada tupla es el name que le pusimos al campo input en el formulario 
    mifichero.close()


def update_item(id, registros, requestForm):
    nuevos_datos = []

    for item in registros:
        if item[0] == str(id):
            nuevos_datos.append([id, requestForm['fecha'], requestForm['concepto'], requestForm['monto']])
        
        else:
            nuevos_datos.append(item)

    fichero_update = open(MOVIMIENTOS_FILE, 'w', newline = '')
    csv_wirter = csv.writer(fichero_update, delimiter=',', quotechar='"')
    csv_wirter.writerows(nuevos_datos)
    fichero_update.close()