import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import NearestNeighbors

# Cargamos los archivos CSV
df_merged = pd.read_csv('merged_data.csv')
df_games = pd.read_csv('games.csv')

# Id de los juegos
game_id = df_games[['id']]

# Características de los juegos en dummies
games_features = df_games[['genres']]

# Utilizamos MultiLabelBinarizer para convertir la columna de géneros en dummies, cada columna representa un género
mlb = MultiLabelBinarizer()
games_features = mlb.fit_transform(games_features['genres'])

# Creamos un modelo de Vecinos más cercanos
knn_model = NearestNeighbors(n_neighbors=6, algorithm='brute') 
knn_model.fit(games_features)

class ProductInput:
    product_id: int