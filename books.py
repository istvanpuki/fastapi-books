from fastapi import FastAPI, HTTPException #importáljuk a FASTAPI keretrendszert
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI() #Azz app változóba hívjuk meg a FastAPI-t

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)

BOOKS = []

#First API
@app.get("/") #Megmondjuk, hogy melyik html metódust használjuk. Az egyik lehetséges paraméter az útvonal, hogy az appunk melyik url-én történjen a (get,post,pust, vagy delete html method)
def read_api():  #Függvényt deklarálunk
    return {"hello": "This is your first FASTAPI app."}

#Get Name API
@app.get("/name" )    # or @app.get("/{name}") You get a dynamic route with the function parameter.
def get_name(name:str):
    return {"Welcome": name}

#Return a list of books
@app.get("/books")
def get_books():
    return BOOKS

#Create a new book.
@app.post("/books")
def create_book(book: Book):
    BOOKS.append(book)

#Update a book
@app.put("/books{book_id}")
def update_book(book_id: UUID, book: Book):
    counter = 0

    for i in BOOKS:
        counter = counter + 1
        if i.id == book_id:
            BOOKS[counter-1] = book
            return BOOKS[counter-1]
    raise HTTPException(
        status_code=404,
        detail=f" ID {book_id} : doesn't exist"
    )

#Delete book
@app.delete("/books/{book_id}")
def delete_book(book_id: UUID, book: Book):
    counter = 0

    for i in BOOKS:
        counter = counter + 1
        if i.id == book_id:
            del BOOKS[counter-1] 
            return f" ID of {book_id} is deleted"
    raise HTTPException(
        status_code=404,
        detail=f" ID {book_id} : doesn't exist"
    )