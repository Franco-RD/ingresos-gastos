from app_ingresos_gastos import app, MOVIMIENTOS_FILE, LAST_ID_FILE
from flask import render_template, request, redirect  
import csv
from datetime import date

#Todas las rutas definidas son de tipo get por default a menos que especifique otro metodo

@app.route("/")
def index():
    datos = []
    fichero = open(MOVIMIENTOS_FILE, 'r') #llamada al archivo csv
    csvReader = csv.reader(fichero, delimiter=',', quotechar='"') #accediendo a cada registro del archivo
    for items in csvReader:
        datos.append(items)  #Recorremos el archivo y agregamos cada linea a la lista datos
    fichero.close()

    return render_template("index.html", data = datos, titulo = "Lista")  #Se pasa la lista como parametro para index.html


@app.route("/new", methods=["GET", "POST"]) #Ahora esta url en particular sirve tanto para metodos get como post. Hay que definir dentro que va a retornar el get y que va a retornar el post
def new():
    if request.method == "POST":  #Esto devuelve el metodo que estamos utilizando 
        comprobar_error = validarFormulario(request.form)
        
        if comprobar_error:
            return render_template("new.html", titulo = "Nuevo", tipoAccion = "registrar", tipoBoton = "Guardar", error = comprobar_error, dataForm = request.form)  #Los datos del formulario se devuelven al html para que en caso de error se mantengan los datos
        
        else:
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
            escritura.writerow([new_id, request.form['fecha'], request.form['concepto'], request.form['monto']])  #request.form es un array de tuplas con todos los datos que cargamos en el formulario. Cada clave de cada tupla es el name que le pusimos al campo input en el formulario 
            mifichero.close()
            return redirect("/")  #Redirect me permite ir a cualquier ruta existente
    
    else: #Si es get
        return render_template("new.html", titulo = "Nuevo", tipoAccion = "registrar", tipoBoton = "Guardar", dataForm = {})  #Como el html siempre usa esos datos del formulario, en los get hay que pasarle el dataForm vacio para que no se rompa
    

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    if request.method == "GET":  #Maneja que pasa con el metodo get
        miFicheroDelete = open(MOVIMIENTOS_FILE, 'r')
        lecturaDelete = csv.reader(miFicheroDelete, delimiter=',', quotechar='"')
        registro_buscado = []
        for item in lecturaDelete:
            if item[0] == str(id):  #Encuentro el id buscado para borrar
                #registro_buscado.append(item)
                registro_buscado = item  #En vez de hacer un append, se iguala el array que devolvemos a item, para que no quede un array de arrays. Asi en delete.html, podemos recorrer con un solo subindice en lugar de dos. 
        
        return render_template("delete.html", titulo = "Borrar", data = registro_buscado)
    
    else: #Maneja que pasa con el metodo post
        ################## Lectura de archivo para dejar todos los datos salvo el del id a borrar ##########################

        fichero_lectura = open(MOVIMIENTOS_FILE, 'r')
        csv_reader = csv.reader(fichero_lectura, delimiter=',', quotechar='"')
        registros = []

        for item in csv_reader:
            if item[0] != str(id):  #Filtro toda la base de datos y la vuelvo a guardar sin el id que quiero borrar
                registros.append(item)                
        fichero_lectura.close()

        ###################### Guardamos todos los registros que quedaron sin el id a borrar ##############################

        fichero_guardar = open(MOVIMIENTOS_FILE, 'w', newline = '')  #El parametro newline es para que vaya haciendo un salto de linea con cada escritura
        csv_writer = csv.writer(fichero_guardar, delimiter=',', quotechar='"')  #Escribir con metodo writer
        for datos in registros:
            csv_writer.writerow(datos)  
        
        fichero_guardar.close()

        return redirect("/")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if request.method == "GET":  #Maneja que pasa con el metodo get
        miFicheroUpdate = open(MOVIMIENTOS_FILE, 'r')
        lecturaUpdate = csv.reader(miFicheroUpdate, delimiter=',', quotechar='"')
        registro_buscado = []
        for item in lecturaUpdate:
            if item[0] == str(id):  #Encuentro el id buscado para actualizar                
                registro_buscado = item

    return render_template("update.html", titulo = "Actualizar", tipoAccion = "actualizar", tipoBoton = "Editar", dataForm = registro_buscado)  #Como el html siempre usa esos datos del formulario, en los get hay que pasarle el dataForm vacio para que no se rompa



def validarFormulario(datosFormulario):
    errores = []
    hoy = str(date.today())  #Fecha del dia para validacion. No se tiene que poder agregar gastos de dias mayores a hoy

    if datosFormulario['fecha'] > hoy or datosFormulario['fecha'] == "":
        errores.append("La fecha no puede ser mayor a la actual o vacia")    
    if datosFormulario['concepto'] == "":
        errores.append("El concepto no puede ir vacio")
    if datosFormulario['monto'] == "" or float(datosFormulario['monto']) == 0.0:  #El monto tiene que ir con int porque por defecto las entradas al formulario son str
        errores.append("El monto debe ser distinto de cero y de vacio")
    
    return errores