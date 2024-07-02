from fastapi import FastAPI, HTTPException
from typing import List
import json

from schema import Book

# File path for storing data
data_file = "books.json"

# Function to read data from file
def read_books_from_file():
    try:
        with open(data_file, "r") as f:
            books = json.load(f)
    except FileNotFoundError:
        books = []
    return books

# Function to write data to file
def write_books_to_file(books):
    with open(data_file, "w") as f:
        json.dump(books, f, indent=4)

# Create FastAPI app instance
app = FastAPI()

# Endpoint to create a new Book
@app.post("/books/", response_model=Book,status_code=201)
async def create_book(book: Book):
    books = read_books_from_file()
    
    # Assigning a new ID
    if not books:
        new_id = 1
    else:
        new_id = max(book['id'] for book in books) + 1
    
    new_book = Book(id=new_id, name=book.name, description=book.description,is_active=book.is_active)
    books.append(new_book.dict())
    
    write_books_to_file(books) 
    return new_book

# Endpoint to read all books
@app.get("/books/", response_model=List[Book])
async def read_books():
    books = []
    data = read_books_from_file()
    for datum in data:
        books.append(datum["id"],datum["name"],datum["description"])
    return books

# Endpoint to read a single Book by id
@app.get("/book/{book_id}", response_model=Book)
async def read_book(book_id: int):
    books = read_books_from_file()
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")