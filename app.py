from flask import Flask, request, jsonify, render_template
from geopy.geocoders import Nominatim
import requests

app = Flask(__name__)
api_key = "50979750b866729860a7abbaead38728"

def buscar_localizacao(nome_lugar):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(nome_lugar)
    if location:
        return location.latitude, location.longitude, location.address
    return None, None, None

def buscar_temperatura(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        temperatura = dados['main']['temp']
        descricao = dados['weather'][0]['description']
        return temperatura, descricao
    return None, None
@app.route('/')
def index():
    return render_template('index.html')    

@app.route('/buscar', methods=['GET'])
def buscar():
    nome = request.args.get('lugar')
    lat, lon, endereco = buscar_localizacao(nome)
    if lat and lon:
        temperatura, descricao = buscar_temperatura(lat, lon, api_key)
        return jsonify({
            "endereco": endereco,
            "latitude": lat,
            "longitude": lon,
            "temperatura": temperatura,
            "descricao": descricao,
            "maps_url": f"https://www.google.com/maps/@{lat},{lon},15z"
        })
    else:
        return jsonify({"erro": "Local não encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)
