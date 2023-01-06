from fastapi import FastAPI, HTTPException, status, Form
from pydantic import BaseModel, Field
from uuid import UUID


class NegativeException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1,
                       max_length=15)
    author: str
    description: str
    rating: int


BOOKS = []


@app.get('/')
async def read_all_books():
    if len(BOOKS) < 1:
        create_books()
    return BOOKS


@app.post("/books/login/")
async def book_login(username: str = Form(), password: str = Form(), book_name: int = Form()):
    if username == 'FastAPIUser' and password == 'test1234!':
        return BOOKS[book_name]
    return "Invalid user"


@app.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.delete('/{book_id}')
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID: {book_id} is deleted'
    raise raise_item_cannot_be_found()


def create_books():
    book_1 = Book(id='d1581f7f-49bd-4cd0-aac1-c9276ebe7236',
                  title='CS 101',
                  author='Frank Lampard',
                  description='From 0 to Hero',
                  rating=10)
    book_2 = Book(id='d2581f7f-49bd-4cd0-aac1-c9276ebe7236',
                  title='CS 102',
                  author='Frank Lampard',
                  description='From 0 to Hero',
                  rating=15)
    book_3 = Book(id='d3581f7f-49bd-4cd0-aac1-c9276ebe7236',
                  title='CS 103',
                  author='Frank Lampard',
                  description='From 0 to Hero',
                  rating=20)
    book_4 = Book(id='d4581f7f-49bd-4cd0-aac1-c9276ebe7236',
                  title='CS 104',
                  author='Frank Lampard',
                  description='From 0 to Hero',
                  rating=30)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


def raise_item_cannot_be_found():
    return HTTPException(status_code=404, detail='Book not found',
                         headers={'X-Header-Error': "Nothing to be seen at the UUID"})
