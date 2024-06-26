#This is main file 
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models

from app import CRUD, database
from . import schemas

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Endpoint to create a new book
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    return CRUD.create_book(db=db, book=book)

# Endpoint to read a list of books
@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return CRUD.get_books(db, skip=skip, limit=limit)

# Endpoint to read a single book by ID
@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = CRUD.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Endpoint to update a book by ID
@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    db_book = CRUD.update_book(db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Endpoint to delete a book by ID
@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = CRUD.delete_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
  

