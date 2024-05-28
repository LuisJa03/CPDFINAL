import matplotlib.pyplot as plt
from pymongo import MongoClient
import numpy as np
from datetime import datetime

# Configuración existente de la conexión a MongoDB
client = MongoClient('localhost', 27017)
db_weather = client['weather_database']
collection_weather = db_weather['weather_data']

# Recuperar datos de MongoDB
datos = list(collection_weather.find())

# Datos para graficar
ciudades = []
temperaturas = []
sensaciones_termicas = []
velocidades_viento = []
fecha_consulta = None  # Para almacenar la fecha de la última consulta

for entrada in datos:
    if all(k in entrada for k in ['city', 'temperature', 'feels_like', 'wind_speed', 'current_date']):
        ciudades.append(entrada['city'])
        temperaturas.append(entrada['temperature'])
        sensaciones_termicas.append(entrada['feels_like'])
        velocidades_viento.append(entrada['wind_speed'])
        # Actualizar la fecha de la última consulta
        fecha_actual = datetime.strptime(entrada['current_date'], "%d/%m/%Y %H:%M:%S")
        if fecha_consulta is None or fecha_actual > fecha_consulta:
            fecha_consulta = fecha_actual

if ciudades:  # Asegurarse de que hay datos para graficar
    x = np.arange(len(ciudades))  # las etiquetas de ubicación en el eje x
    width = 0.35  # el ancho de las barras

    # ConfiG la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Graf temperatura
    ax.bar(x - width/2, temperaturas, width, label='Temperatura (K)', color='b')
    ax.bar(x + width/2, sensaciones_termicas, width, label='Sensación Térmica (K)', color='g')
    ax.set_xlabel('Ciudad')
    ax.set_ylabel('Temperatura y Sensación Térmica (K)')
    ax.set_title('Temperatura y Sensación Térmica por Ciudad')
    ax.set_xticks(x)
    ax.set_xticklabels(ciudades)
    ax.legend()
    
    # fecha de la última consulta
    if fecha_consulta:
        plt.figtext(0.99, 0.01, f'Última consulta: {fecha_consulta.strftime("%d-%m-%Y %H:%M:%S")}', horizontalalignment='right')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Graf velocidad del viento
    plt.figure(figsize=(10, 5))
    plt.bar(ciudades, velocidades_viento, color='r', label='Velocidad del Viento (m/s)')
    plt.title('Velocidad del Viento por Ciudad')
    plt.xlabel('Ciudad')
    plt.ylabel('Velocidad del Viento (m/s)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Fecha de la última consulta
    if fecha_consulta:
        plt.figtext(0.99, 0.01, f'Última consulta: {fecha_consulta.strftime("%d-%m-%Y %H:%M:%S")}', horizontalalignment='right')
    
    plt.show()
else:
    print("No hay datos disponibles para graficar.")
