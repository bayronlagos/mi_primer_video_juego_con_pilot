import requests
# [donde esta la api]----⬇️
base_url = "https://cl.dolarapi.com"
# [protocolo]------⬆️

#ruta o endpoiint que me dice el precio del dolar segun  clp
endpoint_dolar = "/v1/cotizaciones/usd"

#juntamos la url y su endpoint para realizar una peticion tipo GET
respuesta = requests.get(f"{base_url}{endpoint_dolar}")
#                         = https://cl.dolarapi.com/v1/cotizaciones/usd

try:
#serializamos la inofrmacion en json para trabajarla de forma estructurada
    data= respuesta.json()

#mostramos la data rescatada de la respuesta
    print(data)
except:
    print(respuesta)