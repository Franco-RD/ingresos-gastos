from flask import Flask

app = Flask(__name__)

from app_ingresos_gastos.routes import *  #Como todas las rutas tienen que estar por debajo de la declaracion de app, hay que hacer el import de las rutas aca para que esten debajo del app cuando estan en otro arhcivo

'''
Inicializar parametros para servidor de flask (se hace por la terminal)
En windows:   
set FLASK_APP=main.py 
'''
#flask --app main --debug run