import sqlalchemy as db
from sqlalchemy.sql import func
from metadata import create_tables

def search_book(engine:db.engine, user_input:str):
    """
    Takes a search term as input and returns all matching titles, 
    including info about ISBN13 and author.
    """

    book_data = []
    authors, books, authors2books, _, _ = create_tables(engine)

    with engine.connect() as conn: 
        search = "%{}%".format(user_input)
        query = db.select([books.columns.ISBN13, books.columns.Title, func.concat(authors.columns.FirstName, ' ', authors.columns.Initials, ' ', authors.columns.LastName)]).filter(books.columns.Title.like(search)).join(authors2books, books.columns.ISBN13 == authors2books.columns.ISBN13).join(authors, authors2books.columns.AuthorID == authors.columns.ID)
        results = conn.execute(query).fetchall()
    
    for result in results:
        book_data.append(list(result))
    
    return book_data


def stock_info(engine:db.engine, selected_row:int, book_data:list) :
    """
    Takes the selected row number and the book data table as input.
    Matches the stock data on ISBN13 number, 
    and returns the number of books in stock for each store, 
    including info about store name and city.
    """

    stock_data = []
    _, books, _, stores, stock = create_tables(engine)

    selected_row = selected_row
    isbn13 = book_data[selected_row][0]

    with engine.connect() as conn: 
        query = db.select([stores.columns.Name, stores.columns.City, stock.columns.NumberInStock]).filter(books.columns.ISBN13 == isbn13).join(stock, books.columns.ISBN13 == stock.columns.ISBN13).join(stores, stock.columns.StoreID == stores.columns.ID)
        results = conn.execute(query).fetchall()

    for result in results:
        stock_data.append(list(result))
    
    return stock_data
        

