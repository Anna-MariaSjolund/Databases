import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from urllib.parse import unquote
import pyodbc
from sqlalchemy import text
import pandas as pd

server_name   = "localhost"
database_name = "bookstore"

connection_string = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server_name};DATABASE={database_name};uid=bookstoreUser;pwd=veryStrongPassword6293042"
url_string        = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

print('Connecting to database using URL string:')
unquoted_url = unquote(str(url_string))
print(unquoted_url, '\n')

try:    
    engine = create_engine(url_string)
    with engine.connect() as connection:
        print(f'Successfully connected to {database_name}!')
except Exception as e:
    print('Error while connecting to database:\n')
    print(e)

inputed_title = input("Enter book title.")

with engine.connect() as conn: 
    
    metadata = db.MetaData()
    books = db.Table('Books', metadata, autoload=True, autoload_with=engine)
    stock = db.Table('Stock', metadata, autoload=True, autoload_with=engine)
    stores = db.Table('Stores', metadata, autoload=True, autoload_with=engine)

    search = "%{}%".format(inputed_title)

    query = db.select([books.columns.ISBN13, 
                       books.columns.Title, 
                       stores.columns.Name, 
                       stock.columns.NumberInStock]).filter(books.columns.Title.like(search)).join(stock, books.columns.ISBN13 == stock.columns.ISBN13).join(stores, stock.columns.StoreID == stores.columns.ID)

    ResultProxy = conn.execute(query)
    ResultSet = pd.DataFrame(ResultProxy.fetchall())
    
print(ResultSet)