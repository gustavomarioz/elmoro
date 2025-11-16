import requests

fecha1 = "2016-05-28"
fecha2 = "2016-05-29"

url = (
    "https://mercados.ambito.com//dolar/informal/historico-general/"
    + fecha1
    + "/"
    + fecha2
)

respuesta = requests.get(url)
print("respuesta: ", respuesta.json(), " len: ", len(respuesta.json()))
if len(respuesta.json()) > 1:
    cot_usd = respuesta.json()[1][2]
    print("cot_usd: ", cot_usd)
