from urllib import response
from flask import Flask , render_template , request , jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

#Configuracion de la base de datos SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db =SQLAlchemy(app)

#Modelo de la tabla log
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=datetime.utcnow)
    texto = db.Column(db.TEXT)

#Crear la tabla si no existe
with app.app_context():
    db.create_all()

    #prueba1= Log(texto='Mensaje de prueba1')
    #prueba2= Log(texto='Mensaje de prueba2')
    #db.session.add(prueba1)
    #db.session.add(prueba2)
    #db.session.commit()

#Funcion para ordenar los registros por fecha y hora
def ordenar_por_fecha_y_hora(registros):
    return sorted(registros, key = lambda x : x.fecha_y_hora,reverse=True)

@app.route('/')
def index():
    #btener todos los registros de la base de datos
    registros = Log.query.all()
    registos_ordenados = ordenar_por_fecha_y_hora(registros)
    return render_template('index.html',registros=registos_ordenados)

mensajes_log=[]

#funcion para agreagr mensajes y guardar en la base de datos
def agregar_mensajes_log(texto):
    mensajes_log.append(texto)

    #guardar en mensaje en la bd
    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()


#TOKEN DE VERIFICACION PARA LA CONFIGURACION 
TOKEN_ANDERCODE = "ANDERCODE"

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        challenge = verificar_token(request)
        return challenge
    elif request.method == 'POST':
        reponse = recibir_mensajes(request)
        return reponse



def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKEN_ANDERCODE:
        return challenge
    else:
        return jsonify({'error':'Token Invalido !!!!'}),401 

def recibir_mensajes(req):
    req = request.get_json()
    agregar_mensajes_log(req)
     
    return jsonify({'message':'EVENT_RECEIVED'})



#agregar_mensajes_log(json.dumps("test"))

if __name__ =='__main__':
    app.run(host='0.0.0.0',port=80,debug=True)