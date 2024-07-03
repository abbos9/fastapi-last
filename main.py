from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import json
from schema import BookCreateSchema, BookResponseSchema

# File path for storing data
data_file = "books.json"

# Function to read data from file
def read_books_from_file():
    try:
        with open(data_file, "r") as f:
            books = json.load(f)
            # Convert date strings back to datetime objects
            for book in books:
                if isinstance(book.get('created_at'), str):
                    book['created_at'] = datetime.fromisoformat(book['created_at'])
                if isinstance(book.get('updated_at'), str):
                    book['updated_at'] = datetime.fromisoformat(book['updated_at'])
    except FileNotFoundError:
        books = []
    return books

# Function to write data to file
def write_books_to_file(books):
    # Convert datetime objects to ISO format strings
    books = [serialize_book(book) for book in books]
    with open(data_file, "w") as f:
        json.dump(books, f, indent=4)

# Helper function to serialize datetime objects to ISO format strings
def serialize_book(book):
    if isinstance(book.get('created_at'), datetime):
        book['created_at'] = book['created_at'].isoformat()
    if isinstance(book.get('updated_at'), datetime):
        book['updated_at'] = book['updated_at'].isoformat()
    return book

# Create FastAPI app instance
app = FastAPI()

# Endpoint to create a new Book
@app.post("/books/", response_model=BookResponseSchema, status_code=201)
async def create_book(book: BookCreateSchema):
    books = read_books_from_file()
    
    # Assigning a new ID
    if not books:
        new_id = 1
    else:
        new_id = max(b['id'] for b in books) + 1

    new_book = book.copy(update={"id": new_id, "created_at": datetime.now(), "updated_at": datetime.now()})
    books.append(new_book.dict())
    
    write_books_to_file(books)
    return BookResponseSchema(**serialize_book(new_book.dict()))

# Endpoint to read all books
@app.get("/books/", response_model=List[BookResponseSchema])
async def read_books(author: Optional[str] = None):
    books = read_books_from_file()
    if author:
        # Perform case-insensitive search
        matching_books = [book for book in books if author.lower() in book["author"].lower()]
    else:
        matching_books = books
    return [serialize_book(book) for book in matching_books]

# Endpoint to read a single Book by id
@app.get("/book/{book_id}", response_model=BookResponseSchema)
async def read_book(book_id: int):
    books = read_books_from_file()
    for book in books:
        if book['id'] == book_id:
            return serialize_book(book)
    raise HTTPException(status_code=404, detail="Book not found")

# Endpoint to get book statistics
@app.get("/books/stats/")
async def get_book_stats(days: Optional[int] = Query(5)):
    books = read_books_from_file()
    stats = {}
    now = datetime.now()
    
    for book in books:
        days_diff = (now - book['created_at']).days
        if days_diff < days:
            day_str = book['created_at'].strftime("%Y-%m-%d")
            if day_str not in stats:
                stats[day_str] = 0
            stats[day_str] += 1
    
    return stats
