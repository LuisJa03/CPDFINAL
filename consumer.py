from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# Configuración de la conexión a MongoDB
client = MongoClient('localhost', 27017) 

# Conexión a las bases de datos y colecciones específicas
db_weather = client['weather_database']
collection_weather = db_weather['weather_data']

db_marvel = client['marvel']
collection_marvel = db_marvel['characters']

# Configuración del consumidor de Kafka para los topics correctos
consumer = KafkaConsumer(
    'weather_data',  
    'marvel_data',   
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Procesar y almacenar mensajes en las respectivas bases de datos de MongoDB
for message in consumer:
    if message.topic == 'weather_data':
        print("Storing weather data:", message.value)
        collection_weather.insert_one(message.value)  
        print("Weather data stored successfully.")
    elif message.topic == 'marvel_data':
        print("Storing Marvel data:", message.value)
        collection_marvel.insert_one(message.value)  
        print("Marvel data stored successfully.")
