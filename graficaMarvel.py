import matplotlib.pyplot as plt
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db_marvel = client['marvel']
collection_marvel = db_marvel['characters']

# Recuperar datos de MongoDB
data = list(collection_marvel.find())

# Listas para los datos de los gráficos
names = []
comics_counts = []
series_counts = []

for character in data:
    names.append(character['name'])
    comics_counts.append(character['comics'])
    series_counts.append(character['series'])

# Configurar los gráf
fig, ax = plt.subplots(2, 1, figsize=(14, 12))

# Gráfico de cómics
ax[0].bar(names, comics_counts, color='blue')
ax[0].set_title('Número de Cómics por Personaje')
ax[0].set_ylabel('Número de Cómics')
ax[0].set_xticks(range(len(names)))
ax[0].set_xticklabels(names, rotation=90)
ax[0].set_xlabel('Personajes')

# Gráfico de series
ax[1].bar(names, series_counts, color='green')
ax[1].set_title('Número de Series por Personaje')
ax[1].set_ylabel('Número de Series')
ax[1].set_xticks(range(len(names)))
ax[1].set_xticklabels(names, rotation=90)
ax[1].set_xlabel('Personajes')

plt.tight_layout()
plt.show()
