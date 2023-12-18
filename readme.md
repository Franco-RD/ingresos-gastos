# Aplicacion de introducicon a Flask

Programa hecho en python con el framework Flask, Hello world

# Instalacion
- Crear entorno en python y ejecutar el comando
```
pip install -r requirements.txt
```
La libreria utilizada en flask https://flask-wtf.readthedocs.io/en/1.2.x/

# Ejecucion del programa
Inicializar parametros para servidor (se hace por la terminal)
En windows:   
``` set FLASK_APP=main.py ```

# Comando para ejecutar el servidor:   
``` flask --app main run ```

Todo se ejecuta en el servidor web propio del sistema operativo, en un puerto especifico:  * Running on http://127.0.0.1:5000    esto es lo mismo que http://localhost:5000

A veces este puerto esta ocupado por otro programa. 
Para ejecutarlo en otro puerto hay que usar otro comando: 
``` flask --app main run -p 5002 ```   

Si se cambia hay que cambiarlo en las url para ejecutar las funciones

# Comando para ejecutar el servidor en modo debug y ejecutar cambios en tiempo real
``` flask --app main --debug run ```