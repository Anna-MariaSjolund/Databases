import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from urllib.parse import unquote
import pyodbc #do we need this?
from sqlalchemy import text
import pandas as pd
import PySimpleGUI as sg
from sqlalchemy.sql import func

# CONNECTION

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

metadata = db.MetaData()
books = db.Table('Books', metadata, autoload=True, autoload_with=engine)
stock = db.Table('Stock', metadata, autoload=True, autoload_with=engine)
stores = db.Table('Stores', metadata, autoload=True, autoload_with=engine)
authors2books = db.Table('Authors2Books', metadata, autoload=True, autoload_with=engine)
authors = db.Table('Authors', metadata, autoload=True, autoload_with=engine)

# GUI

book_data = []
stock_data = []
book_headings = ['ISBN13', 'Title', 'Firstname']
stock_headings = ['Store', 'Number in Stock']

layout1 = [[sg.Text("Welcome to Paige Turner's Bookstore!", font=('Avenir Next', 30))],
           [sg.Text("Please enter the book title:", font=('Avenir', 15))],
           [sg.InputText(key='-INPUT-', font=('Avenir', 15), size=50)], 
           [sg.Submit('Submit', font=('Avenir', 12)), sg.Button('Exit', key='Exit1', font=('Avenir', 12))]]

layout2 = [[sg.Text('Found the following results:', font=('Avenir', 15))],
           [sg.Table(key='-TABLE1-', values=book_data, headings=book_headings, font=('Avenir', 12), enable_events=True)], 
           [sg.Table(key='-TABLE2-', values=stock_data, headings=stock_headings, font=('Avenir', 12))], 
           [sg.Button('New Search', font=('Avenir', 12)), sg.Button('Exit', key='Exit2', font=('Avenir', 12))]]
#auto_size_columns=False col_width
layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-')]]

window = sg.Window('Bookstore Search', layout, keep_on_top=True, element_justification='c')

layout = 1  # The currently visible layout

while True:
    event, values = window.read()
    print(event, values)

    if event in (None, 'Exit1', 'Exit2'):
        break

    if event == '-TABLE1-':

        stock_data = []

        selected_row = values['-TABLE1-'][0]
        isbn13 = book_data[selected_row][0]
        
        with engine.connect() as conn: 
            
            stock_data = []

            query = db.select([stores.columns.Name, stock.columns.NumberInStock]).filter(books.columns.ISBN13 == isbn13).join(stock, books.columns.ISBN13 == stock.columns.ISBN13).join(stores, stock.columns.StoreID == stores.columns.ID)

            results = conn.execute(query).fetchall()

            for result in results:
                stock_data.append(list(result))

        window['-TABLE2-'].update(values=stock_data)

    if event == 'Submit':
        book_data = []

        # Query data
        with engine.connect() as conn: 

            search = "%{}%".format(values['-INPUT-'])

            query = db.select([books.columns.ISBN13, books.columns.Title, func.concat(authors.columns.FirstName, ' ', authors.columns.Initials, ' ', authors.columns.LastName)]).filter(books.columns.Title.like(search)).join(authors2books, books.columns.ISBN13 == authors2books.columns.ISBN13).join(authors, authors2books.columns.AuthorID == authors.columns.ID)

            results = conn.execute(query).fetchall()
        
        # Change tuple to list
        for result in results:
            book_data.append(list(result))

        # Update layout
        window['-TABLE1-'].update(values=book_data)





        window[f'-COL{layout}-'].update(visible=False)
        layout = layout + 1 
        window[f'-COL{layout}-'].update(visible=True)

    elif event == 'New Search': 
        window['-INPUT-'].update('')
        window[f'-COL{layout}-'].update(visible=False)
        layout = layout -1 
        window[f'-COL{layout}-'].update(visible=True)
        
window.close()