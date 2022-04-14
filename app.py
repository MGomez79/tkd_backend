from ast import Try
from flask import Flask, jsonify, request
from db import Session, engine
from models import Deportista, Usuario
import json
from werkzeug.security import generate_password_hash

app = Flask(__name__)

session = Session()

@app.route('/hola',methods=['GET'])
def hola():
    return jsonify({'message':"Endpoint desde hola"})

@app.route('/create_user', methods=["POST"])
def create_user():
    #print(request)
    #print(dir(request))
    data = json.loads(request.data)
    if 'username' not in data :
        return jsonify({"respuesta":"No estas enviando el username"})
    if 'email' not in data :
        return jsonify({"respuesta":"No estas enviando el email"})   
    if 'password' not in data :
        return jsonify({"respuesta":"No estas enviando el password"})
    if len(data["username"])==0:
        return jsonify({"respuesta":"username no puede estar vacio"})
    if len(data["password"])==0:
        return jsonify({"respuesta":"password no puede estar vacio"})


    # print(data)
    # print(type(data))
    # print(data["username"])
    with engine.connect() as con:
        hash_password = generate_password_hash(data["password"],method="sha256")
        nuevo_usuario = Usuario(username=data["username"],email=data["email"],password=hash_password)
        session.add(nuevo_usuario)
        try:
            session.commit()
        except:
            return jsonify({"respuesta":"El usuario ya esta creado en nuestra base de datos"})
    return jsonify({"respuesta": "Usuario creado correctamente"})

@app.route('/cargar_datos', methods=["POST"])
def cargar_datos():
    #print(request)
    #print(dir(request))
    data = json.loads(request.data)
    #if 'id_documento' not in data :
       # return jsonify({"respuesta":"No estas enviando el numero de documento"})
    if 'categoria' not in data :
        return jsonify({"respuesta":"No estas enviando la categoria"})   
    if 'peso' not in data :
        return jsonify({"respuesta":"No estas enviando el peso"})
    #if 'edad' not in data :
        #return jsonify({"respuesta":"No estas enviando la edad"})
    if 'estatura' not in data :
        return jsonify({"respuesta":"No estas enviando la estatura"})
    #if len(data["id_documento"])==0:
        #return jsonify({"respuesta":"numero de documento no puede estar vacio"})
    if len(data["categoria"])==0:
        return jsonify({"respuesta":"categoria no puede estar vacio"})
    if len(data["peso"])==0:
        return jsonify({"respuesta":"peso no puede estar vacio"})
    #if len(data["edad"])==0:
        #return jsonify({"respuesta":"edad no puede estar vacio"})
    if len(data["estatura"])==0:
        return jsonify({"respuesta":"estatura no puede estar vacio"})

    print(data)
    print(type(data))
    print(data["id_documento"])
    with engine.connect() as con:
        nuevo_deportista = Deportista(id_documento=data["id_documento"],categoria=data["categoria"],peso=data["peso"],edad=data["edad"],estatura=data["estatura"])
        session.add(nuevo_deportista)
        try:
            session.commit()
        except:
            return jsonify({"respuesta":"El deportista ya esta creado en nuestra base de datos"})
    return jsonify({"respuesta": "Deportista creado correctamente"})

@app.route('/obtener_edad',methods=['GET'])
def obtener_datos():
    data = json.loads(request.data)
    print(data)
    if 'username' not in data:
        return jsonify({"respuesta":"username no enviado, validar datos"})
    with engine.connect() as con:
        obtener_usuario = f"select * from usuario where username = '{data['username']}'"
        try:
            respuesta = con.execute(obtener_usuario).one()
        except:
            return jsonify({"respuesta":"El usuario no esta en nuestra base de datos"})
        print(respuesta)
        obtener_edad = f"select edad from deportista where username_id = '{respuesta[0]}'"
        respuesta_deportista = con.execute(obtener_edad)
        respuesta_deportista = [i[0]for i in respuesta_deportista]
        return jsonify({"deportista_usuario":{"usuario":data['username'],"deportista":respuesta_deportista}})

if __name__ == "__main__":
    app.run(debug=True)