import json
import os
import random
from typing import Literal, Optional
from uuid import uuid4
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from fastapi import FastAPI, HTTPException

#Segue a fastapi
app = FastAPI()

#Define classe Book
class Book (BaseModel):
    name: str
    price: float
    #Gera ID unico
    book_id: Optional[str] = uuid4().hex
    genre: Literal['fiction', 'non-finction']

BOOK_DATABASE = []

#Define a variavel para armazenar os livros da lista em json
BOOKS_FILE = 'books.json'

#Verifica se o arquivo BOOKS-FILE existe e, se sim, carrega o BOOK_DATABASE nele
if os.path.exists(BOOKS_FILE):
    #Abre o arquivo para leitura
    with open (BOOKS_FILE, 'r') as f:
        #Le o conteudo do json e atualiza BOOK_DATABASE
        BOOK_DATABASE = json.load(f)

# /           -> boas vindas
@app.get("/")
async def home():
    return "Welcome to my bookstore"

# /list-books     -> lista todos os livros
@app.get("/list-books")
async def list_books():
    return {"books": BOOK_DATABASE}

# /list-book-by-index/{index} -> listar um livro especifico por indice
@app.get("/list-book-by-index/{index}")
async def list_book_by_index(index: int):
    #Tratativa de erro
    if index <0 or index >=len(BOOK_DATABASE):
        raise HTTPException(404, "Index out of range")
    else:
        return { "books": BOOK_DATABASE[index]}

# /get-random-book   -> livro aleatorio
@app.get("/get-random-book/")
async def get_random_book():
    return random.choice(BOOK_DATABASE)
    
# /add-book     -> adicionar novo livro
@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)
    #Atualizo o json com novo livro
    with open (BOOKS_FILE, 'w') as f:
        json.dump(BOOK_DATABASE, f)
    return {'message': f'Book {book} was added'}