from fastapi import FastAPI
from data_loader import df_merged, game_id, games_features, df_games, knn_model

app = FastAPI(title = "Steam Data Consults")

@app.get("/PlayTimeGenre")
def PlayTimeGenre(genero: str):
    # Filtrar el DataFrame por el género especificado
    games_by_genre = df_merged[df_merged['genres'].str.contains(genero, case=False, na=False, regex=r'\b' + genero + r'\b')]

    if games_by_genre.empty:
        return {"mensaje": "No se encontraron juegos para el género especificado"}

    # Agrupar por año y sumar las horas jugadas
    playtime_by_year = games_by_genre.groupby('release_year')['playtime_forever'].sum()

    # Encontrar el año con más horas jugadas
    year_with_most_playtime = playtime_by_year.idxmax()

    # Convertir year_with_most_playtime a tipo int
    year_with_most_playtime = int(year_with_most_playtime)

    return {"Año de lanzamiento con más horas jugadas para el género": year_with_most_playtime}

@app.get("/UserForGenre")
def UserForGenre(genero: str):
    # Filtrar el DataFrame por el género especificado
    games_by_genre = df_merged[df_merge['genres'].str.contains(genero, case=False, na=False, regex=r'\b' + genero + r'\b')]

    if games_by_genre.empty:
        return {"mensaje": "No se encontraron juegos para el género especificado"}

    # Encontrar el usuario con más horas jugadas para el género
    user_with_most_playtime = games_by_genre.groupby('user_id')['playtime_forever'].sum().idxmax()

    # Filtrar el DataFrame por el usuario con más horas jugadas
    user_most_playtime_df = games_by_genre[games_by_genre['user_id'] == user_with_most_playtime]

    # Calcular la acumulación de horas jugadas por año
    playtime_by_year = user_most_playtime_df.groupby('release_year')['playtime_forever'].sum()

    # Convertir el resultado en un diccionario
    result = {
        "Usuario con más horas jugadas para el género": user_with_most_playtime,
        "Acumulación de horas jugadas por año": playtime_by_year.to_dict()
    }

    return result

@app.get("/UsersRecommend")
def UsersRecommend(año: int):
    # Filtrar el DataFrame por el año dado y condiciones de recomendación y sentimiento positivo/neutro
    juegos_recomendados = df_merged[(df_merged['release_year'] == año) & (df_merged['recommend'] == True) & (df_merged['sentiment_analysis'] >= 1)]

    if juegos_recomendados.empty:
        return {"mensaje": "No se encontraron juegos recomendados para el año y condiciones especificados"}

    # Agrupar los juegos por título y contar la cantidad de recomendaciones
    juegos_agrupados = juegos_recomendados.groupby('title')['recommend'].sum().reset_index()

    # Ordenar los juegos por cantidad de recomendaciones en orden descendente
    juegos_agrupados = juegos_agrupados.sort_values(by='recommend', ascending=False)

    # Tomar los tres primeros juegos
    top_3_juegos = juegos_agrupados.head(3)

    # Crear la lista de resultados en el formato deseado
    resultados = [{"Puesto {}".format(i + 1): juego['title']} for i, (_, juego) in enumerate(top_3_juegos.iterrows())]

    return resultados

@app.get("/UsersNotRecommend")
def UsersNotRecommend(año: int):
    # Filtrar el DataFrame por el año dado y condiciones de no recomendación y sentimiento negativo
    juegos_no_recomendados = df_merged[(df_merged['release_year'] == año) & (df_merged['recommend'] == False) & (df_merged['sentiment_analysis'] < 1)]

    if juegos_no_recomendados.empty:
        return {"mensaje": "No se encontraron juegos no recomendados para el año y condiciones especificados"}

    # Agrupar los juegos por título y contar la cantidad de no recomendaciones
    juegos_agrupados = juegos_no_recomendados.groupby('title')['recommend'].sum().reset_index()

    # Ordenar los juegos por cantidad de no recomendaciones en orden descendente
    juegos_agrupados = juegos_agrupados.sort_values(by='recommend', ascending=False)

    # Tomar los tres primeros juegos
    top_3_juegos = juegos_agrupados.head(3)

    # Crear la lista de resultados en el formato deseado
    resultados = [{"Puesto {}".format(i + 1): juego['title']} for i, (_, juego) in enumerate(top_3_juegos.iterrows())]

    return resultados

@app.get("/sentiment_analysis")
def sentiment_analysis(año: int):
    # Filtrar el DataFrame por el año dado
    juegos_por_año = df_merged[df_merged['release_year'] == año]

    if juegos_por_año.empty:
        return {"mensaje": "No se encontraron juegos para el año especificado"}

    # Convertir los valores de la columna sentiment_analysis a tipo int
    juegos_por_año['sentiment_analysis'] = juegos_por_año['sentiment_analysis'].astype(int)

    # Contar la cantidad de registros de reseñas de usuarios con diferentes categorías de sentimiento
    sentiment_counts = juegos_por_año['sentiment_analysis'].value_counts()

    # Crear un diccionario con el resultado en el formato deseado
    resultado = {
        "Negative": int(sentiment_counts.get(0, 0)),
        "Neutral": int(sentiment_counts.get(1, 0)),
        "Positive": int(sentiment_counts.get(2, 0))
    }

    return resultado

@app.post("/recomendacion_juego/")
def recomendacion_juego(product_id: int):
    try:
        # Encuentra el índice del juego con el ID proporcionado
        game_index = game_id.index[game_id['id'] == product_id].tolist()[0]

        # Encuentra los juegos más cercanos utilizando KNN
        _, indices = knn_model.kneighbors(games_features[game_index:game_index+1], n_neighbors=6)

        # Obtiene los IDs de los juegos recomendados (excluyendo el juego de consulta)
        recommended_game_ids = [df_games.iloc[i]['id'] for i in indices[0] if i != game_index]

        return {"recommended_game_ids": recommended_game_ids}
    except Exception as e:
        return {"error": str(e)}