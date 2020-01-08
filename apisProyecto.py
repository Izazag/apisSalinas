#!/usr/bin/env python
import os
import cv2
import json
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import functions as fn

app = Flask(__name__)
doctors_dict = ""
users_dict = ""
PORT = 9097

@app.route('/getDoctors', methods = ['GET'])
def get_doctors():
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
	email = "jmontesi1@outlook.com"
	if fn.checkLogin(user_dict, email):
		return True
	return False

@app.route('/register', methods = ['POST'])
def registro():
    return True

# @app.route('/updateInfo', methods = ['POST'])
# def update_info():
#     data = request.json()
#     data.('id')
    

if __name__ == '__main__':
    with open('doctores.json', 'r') as f:
        doctors_dict = json.load(f)
        
    with open('usuarios.json', 'r') as f:
        users_dict = json.load(f)
    app.run(host = '0.0.0.0', port = PORT, threaded = True, debug = True)





