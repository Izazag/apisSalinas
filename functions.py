from datetime import *
import json

def checkLogin(jsonData, email, password):
    for user in jsonData:
        if email == user.get('email'):
            if checkPass(user.get('password'), password):
                return user.get('id'), user.get('isDoctor')
    return -1, False

def checkEmail(email, emailsList):
    for emails in emailsList:
        if email == emails.get('email'):
            return True
    return False
            

def checkPass(passSaved, passIn):
    if passSaved == passIn:
        return True
    return False

def cambiarDisp(idFecha, idDoctor, fechas_dict):
    fechas_aux = list()
    for fecha in fechas_dict:
        if idFecha == fecha['fecha'] and idDoctor == fecha['idDoctor']:
            fecha['disponible'] = False
            fechas_aux.append(fecha)
            print(fecha)
        else:
            fechas_aux.append(fecha)
            print(fecha)
    return fechas_aux

def fechasDoctor(id, fechas_dict):
    fechas_aux = list()
    for fecha in fechas_dict:
        if fecha['idDoctor'] == id and compareDates(fecha['fecha']):
            fechas_aux.append(fecha)
        if fecha['disponible'] == False:
            continue
    return fechas_aux
            
def compareDates(fecha):
    date_time_obj = datetime.strptime(fecha, '%Y-%m-%d %H:%M')
    if datetime.today() < date_time_obj:
        return True
    return False

def getCitas(idUsuario, citas_dict):
    citas_aux = list()
    for cita in citas_dict:
        if idUsuario == cita['idUsuario'] and compareDates(cita['fecha']):
            citas_aux.append(cita)
    return citas_aux

def getCitasPasadas(idUsuario, citas_dict):
    citas_aux = list()
    for cita in citas_dict:
        if idUsuario == cita['idUsuario'] and not compareDates(cita['fecha']):
            citas_aux.append(cita)
    return citas_aux

def getLastID(dict_list):
    x = 0
    for i in dict_list:
        n = i.get('id')
        if (type(n) == type(x)):
            if n > x:
                x = n
    return x + 1

def saveToFile(filename, jsonData):
	with open(filename, 'r+') as f:
		f.write(jsonData)
		f.close()
