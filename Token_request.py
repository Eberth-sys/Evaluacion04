print("Proyecto de Eberth Alarcòn")

import requests
import json
import conf
import time

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
try:
    API_TOKEN = Token_request(conf.user, conf.password)
except Exception as err:
    print("Error en data API")
    exit (1)

#print("")
#print("***" *200)
#print("EL TOKEN ES:", API_TOKEN)
#print("***" *200)

#GET http://apic-ip-address/api/class/topSystem.json
while True:
    # Monitorar la RED cada 5 minutos, en busca de algun evento extraño.
    time.sleep(300) #300 segundo equivalen a 5 minutos del tiempo que necesitamos.

url_top = "https://10.10.20.14/api/class/topSystem.json"
cabecera_top= {"content-type":"application/json"}
webtoken_top= { "APIC-Cookie": Token_request(conf.user, conf.password)}
respuesta_top= requests.get(url_top, headers=cabecera_top, cookies=webtoken_top, verify=False)
respuesta_top_json= respuesta_top.json()
total_equipos_json= respuesta_top_json["totalCount"]
total_equipos_json = int(total_equipos_json)
#print(respuesta_top_json)
try:
    name = respuesta_top_json["imdata"][0]["topSystem"]["attributes"]["name"]
    tiempo = respuesta_top_json["imdata"][0]["topSystem"]["attributes"]["modTs"]
    ip = respuesta_top_json["imdata"][0]["topSystem"]["attributes"]["address"]
    mac = respuesta_top_json["imdata"][0]["topSystem"]["attributes"]["fabricMAC"]
    state = respuesta_top_json["imdata"][0]["topSystem"]["attributes"]["state"]
except Exception as err:
    print(" - -> Error en la URL, por favor corrobar dicha informaciòn < - -")
    exit(1)
print("")
print(" Cantidad de equipos operativos de la RED: ", total_equipos_json)
print("")
print("////"*20)
print("              Identificacion Servidor Controlador Disponible")
print("////"*20)
print("- Nombre del servidor :", name)
print("- Direcciòn IP :", ip)
print("- Direcciòn MAC :", mac)
print("- Estado actual :", state)
print("- Tiempo operativo :", tiempo)
print("*-*-"*20)
print("")

#Si existe un número mayor que 4 de equipos en la red debe ser notificado.
if total_equipos_json > 4:
    print(" ## ALERTA ## Se ha detectado nuevos equipos dentro de nuestra red")
    print(" ## ALERTA ## Se ha notificado al administrador de la red")

#Si el servidor Controlador Cae, deberà ser notificado.
if state != "in-service":
    print(" ## ALERTA ## Se ha detectado que el servidor CONTROLADOR no esta disponible")
    print(" ## ALERTA ## Se ha notificado al administrador de la red")