from app_ingresos_gastos import app, MOVIMIENTOS_FILE, LAST_ID_FILE
from flask import render_template, request, redirect  
import csv
from datetime import date
from app_ingresos_gastos.models import *

#Todas las rutas definidas son de tipo get por default a menos que especifique otro metodo

@app.route("/")
def index():
    datos = select_all()
    return render_template("index.html", data = datos, titulo = "Lista")  #Se pasa la lista como parametro para index.html


@app.route("/new", methods=["GET", "POST"]) #Ahora esta url en particular sirve tanto para metodos get como post. Hay que definir dentro que va a retornar el get y que va a retornar el post
def new():
    if request.method == "POST":  #Esto devuelve el metodo que estamos utilizando 
        comprobar_error = validarFormulario(request.form)
        
        if comprobar_error:
            return render_template("new.html", titulo = "Nuevo", tipoAccion = "registrar", tipoBoton = "Guardar", error = comprobar_error, dataForm = request.form)  #Los datos del formulario se devuelven al html para que en caso de error se mantengan los datos
        
        else:            
            insert(request.form)
            return redirect("/")  #Redirect me permite ir a cualquier ruta existente
    
    else: #Si es get
        return render_template("new.html", titulo = "Nuevo", tipoAccion = "registrar", tipoBoton = "Guardar", dataForm = {}, urlForm = "/new")  #Como el html siempre usa esos datos del formulario, en los get hay que pasarle el dataForm vacio para que no se rompa
    

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    if request.method == "GET":  #Maneja que pasa con el metodo get
        registro_buscado = select_by(id, "==")
        return render_template("delete.html", titulo = "Borrar", data = registro_buscado)
    
    else: #Maneja que pasa con el metodo post
        ################## Lectura de archivo para dejar todos los datos salvo el del id a borrar ##########################
        registros = select_by(id, "!=")

        ###################### Guardamos todos los registros que quedaron sin el id a borrar ##############################
        delete_by(id, registros=registros)

        return redirect("/")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if request.method == "POST":  #Maneja que pasa con el metodo post
        formulario = request.form
        registros = select_all()
        update_item(id, registros, formulario)
        
        return redirect("/")
    
    else:  #Maneja que pasa con el metodo get
        registro_buscado = select_by(id, "dic")   

        return render_template("update.html", titulo = "Actualizar", tipoAccion = "actualizar", tipoBoton = "Editar", dataForm = registro_buscado, urlForm = f"/update/{id}")  



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