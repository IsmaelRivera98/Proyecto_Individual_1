# Steam Data API

Este es un proyecto de API basado en FastAPI que proporciona consultas relacionadas con datos de juegos de Steam. El proyecto se divide en dos archivos principales:

## data_loader.py

Este archivo se encarga de cargar y procesar los datos necesarios para el funcionamiento de la API. Aquí se realiza lo siguiente:

- Carga los datos desde los archivos CSV (`merged_data.csv` y `games.csv`).
- Selecciona las columnas relevantes, como el ID de los juegos y las características de los juegos.
- Utiliza `MultiLabelBinarizer` para convertir la columna de géneros en características binarias.
- Crea un modelo de `NearestNeighbors` para recomendaciones de juegos.

## main.py

Este archivo contiene la implementación de la API FastAPI y define las rutas y funciones para realizar consultas relacionadas con los juegos. Las rutas disponibles son:

- `/PlayTimeGenre`: Obtiene el año de lanzamiento con más horas jugadas para un género específico.
- `/UserForGenre`: Encuentra el usuario con más horas jugadas para un género específico y muestra la acumulación de horas jugadas por año.
- `/UsersRecommend`: Devuelve los juegos recomendados para un año específico según las condiciones especificadas.
- `/UsersNotRecommend`: Devuelve los juegos no recomendados para un año específico según las condiciones especificadas.
- `/sentiment_analysis`: Muestra el análisis de sentimiento de las reseñas de usuarios para un año específico.
- `/recomendacion_juego`: Proporciona recomendaciones de juegos similares para un juego específico.

## Uso de la API

Para utilizar la API, asegúrate de tener todas las dependencias instaladas y ejecuta el archivo `main.py` para iniciar el servidor FastAPI. Luego, puedes realizar solicitudes HTTP a las rutas mencionadas anteriormente para obtener información relacionada con los juegos.
