#app para demostrar el uso de Flask utilizando rutas básicas y una conexión a una base de datos Mysql.
#el ejercicio es: crear una API RESTful para gestionar el recurso "productos" en la base de datos.

from flask import Flask, Blueprint
from rutas.rutas_productos import productos_bp

app = Flask(__name__)

app.register_blueprint(productos_bp)

if __name__ == '__main__':
    app.run(debug=True)
