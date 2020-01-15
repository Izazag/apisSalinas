#!/usr/bin/env python
import os
import cv2
import json
from flask import Flask, jsonify, request
import functions as fn

# from OpenSSL import SSL
# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')

app = Flask(__name__)
doctors_dict = ""
users_dict = ""
creds_dict = ""
fechas_dict = ""
citas_dict = ""
PORT = 9097
usuarios = "usuarios.json"
citas = "citas.json"
doctores = "doctores.json"
fechas = "fechas.json"
credenciales = "credenciales.json"

@app.route('/getDoctors', methods = ['GET'])
def get_doctors():
    print(doctors_dict)
    data = doctors_dict
    return jsonify(data)

@app.route('/getDoctors/<id>', methods = ['GET'])
def get_spec_doctors(id):
    id = int(id)
    data = doctors_dict
    for index, doctors in enumerate(data):
        if index == id - 1:
            return doctors
    return data[0]

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    x, isDoc = fn.checkLogin(creds_dict, email, password)
    if x > 0:
        return jsonify({"isDoctor": isDoc, "id": x})
    return jsonify({"isDoctor": 0, "id": -1})

@app.route('/nuevaCita', methods = ['POST'])
def crearCita():
    data = request.get_json()
    print(data)
    fecha = data.get('fecha')
    idDoctor = data.get('idDoctor')
    idUsuario = data.get('idUsuario')
    
    fechas_aux = fn.cambiarDisp(fecha, idDoctor, fechas_dict)
    
    data.__setitem__('id', fn.getLastID(citas_dict))
    citas_dict.append(data)
    
    fn.saveToFile(citas, json.dumps(citas_dict))
    fn.saveToFile(fechas, json.dumps(fechas_aux))
    
    fechas_dict = fechas_aux
    
    return '{"respuesta" : "Cita Registrada"}'

@app.route('/getFechas/<id>', methods = ['GET'])
def getFechas(id):
    return jsonify(fn.fechasDoctor(int(id), fechas_dict))

@app.route('/getCitas/<id>', methods = ['GET'])
def getCitas(id):
    return jsonify(fn.getCitas(int(id), citas_dict))

@app.route('/getCitasPasadas/<id>', methods = ['GET'])
def getCitasPasadas(id):
    return jsonify(fn.getCitasPasadas(int(id), citas_dict))

@app.route('/registro', methods = ['POST'])
def registro():
    data = request.get_json()
    
    if not fn.checkEmail(data.get('email'), creds_dict):
    
        creds_aux = {'id:': fn.getLastID(creds_dict),
                            'email': data.get('email'),
                            'password': data.get('password'),
                            'isDoctor': False}
        
        del data['email']
        del data['password']
        
        data.__setitem__('id', fn.getLastID(users_dict))
        data.__setitem__('userId', fn.getLastID(creds_dict))
        
        users_dict.append(data)
        creds_dict.append(creds_aux)
        
        print(json.dumps(users_dict))
        
        fn.saveToFile(usuarios, json.dumps(users_dict))
        fn.saveToFile(credenciales, json.dumps(creds_dict))
    
        return '{"response" : "Registro correcto"}'
    
    return '{"response" : "Correo Ocupado"}'

def openFile(filename, dictionary):
    with open(filename, 'r+') as f:
        dictionary = json.load(f)
        f.close()

if __name__ == '__main__':
    with open(doctores, 'r+') as f:
        doctors_dict = json.load(f)
        f.close()
    with open(usuarios, 'r+') as f:
        users_dict = json.load(f)
        f.close()
    with open(fechas, 'r+') as f:
        fechas_dict = json.load(f)
        f.close()
    with open(citas, 'r+') as f:
        citas_dict = json.load(f)
        f.close()
    with open(credenciales, 'r+') as f:
        creds_dict = json.load(f)
        f.close()
    app.run(host = '0.0.0.0', port = PORT, threaded = True, debug = True)
            # ssl_context=('cert.pem', 'key.pem'))
