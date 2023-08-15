print("Proyecto de Eberth Alarcòn")

import requests
import json
import conf

def Token_request(user,password):

    url_login = "https://10.10.20.14/api/aaaLogin.json"

    data = {
        "aaaUser" : {
            "attributes" : {
                "name" : user,
                "pwd" : password
            }
        }
    }

    cabecera = {"content-type":"application/json"}

    requests.packages.urllib3.disable_warnings() # Eliminar el warning

    Respuesta= requests.post(url_login, json.dumps(data), headers=cabecera, verify=False)
    Respuesta_json= Respuesta.json()
    # print(Respuesta_json)
    API_TOKEN = Respuesta_json["imdata"][0]["aaaLogin"]["attributes"]["token"]
    return API_TOKEN
API_TOKEN = Token_request(conf.user, conf.password)

#print("")
#print("***" *200)
#print("EL TOKEN ES:", API_TOKEN)
#print("***" *200)

#GET http://apic-ip-address/api/class/topSystem.json

url_top = "https://10.10.20.14/api/class/topSystem.json"
cabecera_top= {"content-type":"application/json"}
webtoken_top= { "APIC-Cookie": Token_request(conf.user, conf.password)}
respuesta_top= requests.get(url_top, headers=cabecera_top, cookies=webtoken_top, verify=False)
respuesta_top_json=  respuesta_top.json()
#print(respuesta_top_json)
name = respuesta_top_json["imdata"][0]["topSystem"]["attributes"]["name"]
tiempo = respuesta_top_json["imdata"][0]["topSystem"]["attributes"]["modTs"]
ip = respuesta_top_json["imdata"][0]["topSystem"]["attributes"]["address"]
mac = respuesta_top_json["imdata"][0]["topSystem"]["attributes"]["fabricMAC"]
state = respuesta_top_json["imdata"][0]["topSystem"]["attributes"]["state"]
print("")
print("*-*-"*20)
print("Identificacion Servidor Controlador Disponible")
print("")
print("- Nombre del servidor :", name)
print("- Direcciòn IP :", ip)
print("- Direcciòn MAC :", mac)
print("- Estado actual :", state)
print("- Tiempo operativo :", tiempo)
print("*-*-"*20)
print("")