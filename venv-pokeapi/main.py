from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import requests

app = FastAPI()
app.title = "Práctica SP"
app.version = "1.0"


#Query pokemon por rango
@app.get('/pokemon', tags=['pokemon'])
def get_pokemon(limit: int, offset: int):
    pokedata = requests.get(url=f'https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}').json()
    return pokedata 

#Query pokemon por nombre
@app.get('/pokemon/{name}', tags=['pokemon'])
def get_pokemon(name: str):
    pokedata = requests.get(url=f'https://pokeapi.co/api/v2/pokemon/{name}').json()
    return pokedata

#Ejemplos Create, Read, Update y Delete

#Creación de esquema
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max=15, min = 5)
    overview: str
    year: int
    rating: float
    category: str

#Lista de películas
movies = [
    {
    "id":1,
    "title": "Avatar",
    "overview":"En un exuberante planeta llamado Pandora viven los Na'vi",
    "year": "2009",
    "rating": 7.8,
    "category": "Accion"
    },
      {
    "id":2,
    "title": "Avatar",
    "overview":"En un exuberante planeta llamado Pandora viven los Na'vi",
    "year": "2009",
    "rating": 7.8,
    "category": "Accion"
    }
]

#Query lista de películas
@app.get('/movies', tags=['movies'])
def get_movies():
    return JSONResponse(content=movies)

#Query película por id
@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[])
   
#Query películas por categoría
@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
    data = [item for item in movies if item['category'] == category]
    return JSONResponse(content=data)

#Crear películas
@app.post('/movies/', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={"message": "Se ha registrado la película"})

#Modificar películas
@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie): 
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(content={"message": "Se ha modificado la película"})

#Eliminar películas
@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Se ha eliminado la película"})
