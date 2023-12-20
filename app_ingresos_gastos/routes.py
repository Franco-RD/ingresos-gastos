from app_ingresos_gastos import app
from flask import render_template, request, redirect  
import csv

#Todas las rutas definidas son de tipo get por default a menos que especifique otro metodo

@app.route("/")
def index():
    datos = []
    fichero = open('data/movimientos.csv', 'r') #llamada al archivo csv
    lectura = csv.reader(fichero, delimiter=',', quotechar='"') #accediendo a cada registro del archivo
    for items in lectura:
        datos.append(items)  #Recorremos el archivo y agregamos cada linea a la lista datos

    return render_template("index.html", data = datos, titulo = "Lista")  #Se pasa la lista como parametro para index.html

@app.route("/new", methods=["GET", "POST"]) #Ahora esta url en particular sirve tanto para metodos get como post. Hay que definir dentro que va a retornar el get y que va a retornar el post
def new():
    if request.method == "POST":  #Esto devuelve el metodo que estamos utilizando 
        mifichero = open('data/movimientos.csv', 'a', newline = '')  #Acceder al archivo y configurar para cargarle registros 
        escritura = csv.writer(mifichero, delimiter=',', quotechar='"')  #Escribir con metodo writer
        escritura.writerow([request.form['fecha'], request.form['concepto'], request.form['monto']])  #request.form es un array de tuplas con todos los datos que cargamos en el formulario. Cada clave de cada tupla es el name que le pusimos al campo input en el formulario 
        mifichero.close()
        return redirect("/")  #Redirect me permite ir a cualquier ruta existente
    else:
        return render_template("new.html", titulo = "Nuevo", tipoAccion = "registrar", tipoBoton = "Guardar")

@app.route("/delete")
def delete():
    return render_template("delete.html", titulo = "Borrar")

@app.route("/update")
def update():
    return render_template("update.html", titulo = "Actualizar", tipoAccion = "actualizar", tipoBoton = "Editar")