print("Proyecto de Eberth Alarcòn")

import requests
import json
import conf

def Token_request():

    url_login = "https://10.10.20.14/api/aaaLogin.json"

    data = {
        "aaaUser" : {
            "attributes" : {
                "name" : conf.user,
                "pwd" : conf.password
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
API_TOKEN = Token_request()

print("")
print("***" *200)
print("EL TOKEN ES:", API_TOKEN)
print("***" *200)


