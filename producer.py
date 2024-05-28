from datetime import date
from datetime import datetime
import json
import requests
from kafka import KafkaProducer

# Configura el productor de Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# API URL y clave
api_key = 'bf84aa03063701e1669405af06a95c64'
cities = {
    "Parral": {"lat": 26.933354, "lon": -105.666984},
    "Delicias": {"lat": 28.190130, "lon": -105.470121},
    "Chihuahua": {"lat": 28.633333, "lon": -106.083333}
}

def fetch_weather_data():
    now = datetime.now()
    for city_name, coords in cities.items():
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={coords['lat']}&lon={coords['lon']}&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            selected_data = {
                "city": city_name,
                "temperature": weather_data['main']['temp'],
                "feels_like": weather_data['main']['feels_like'],
                "wind_speed": weather_data['wind']['speed'],
                "current_date": "{}/{}/{}  {:02d}:{:02d}:{:02d}".format(now.day, now.month, now.year, now.hour, now.minute, now.second)
            }
            # Envia los datos al topic 'weather_data' en Kafka
            producer.send('weather_data', value=selected_data)
            producer.flush()  # Corroborar que todos los mensajes se han enviado
            print(f"Data sent to Kafka successfully for {city_name}")
        else:
            print(f"Failed to fetch weather data for {city_name}")
            print("HTTP Status Code:", response.status_code)
            print("Response Content:", response.text)  

# Llama a la función para obtener y enviar datos
fetch_weather_data()

# URL de la API de Marvel
url = "https://gateway.marvel.com:443/v1/public/characters?ts=1&apikey=072e8432598f2f2499fe234012fb38c4&hash=c0af73530b8b44ba2845f2204888c518"

def fetch_marvel_data():
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        characters = data['data']['results']
        for character in characters:
            # Extraer los datos requeridos del personaje
            character_data = {
                'id': character['id'],
                'name': character['name'],
                'comics': character['comics']['available'],
                'series': character['series']['available']
            }
            # Enviar los datos al topic de Kafka
            producer.send('marvel_data', value=character_data)
            print(character_data)
            producer.flush()
        print("Data sent to Kafka successfully")
    else:
        print("Failed to fetch data from Marvel API")
        print("HTTP Status Code:", response.status_code)
        print("Response Content:", response.text)


fetch_marvel_data()