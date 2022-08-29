import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from urllib.parse import unquote
import pyodbc
from sqlalchemy import text
import pandas as pd
import PySimpleGUI as sg

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


# GUI

data = []
headings = ['ISBN13', 'Title', 'Store', 'Number in Stock']

layout1 = [[sg.Text("Welcome to Paige Turner's Bookstore")],
           [sg.Text("Please enter book title.")],
           [sg.InputText(key='Input')], 
           [sg.Submit('Submit'), sg.Button('Exit', key='Exit1')]]

layout2 = [[sg.Text('Found the following results:')],
           [sg.Table(key='-TABLE-', values=data, headings=headings)], 
           [sg.Button('New Search'), sg.Button('Exit', key='Exit2')]]

layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-')]]

window = sg.Window('Bookstore Search', layout, margins=(300, 150))

layout = 1  # The currently visible layout

while True:
    event, values = window.read()
    print(event, values)

    

    if event in (None, 'Exit1', 'Exit2'):
        break

    if event == 'Submit':

        window['-TABLE-'].update('')
        # Query data
        with engine.connect() as conn: 
            metadata = db.MetaData()
            books = db.Table('Books', metadata, autoload=True, autoload_with=engine)
            stock = db.Table('Stock', metadata, autoload=True, autoload_with=engine)
            stores = db.Table('Stores', metadata, autoload=True, autoload_with=engine)

            search = "%{}%".format(values['Input'])

            query = db.select([books.columns.ISBN13, 
                            books.columns.Title, 
                            stores.columns.Name, 
                            stock.columns.NumberInStock]).filter(books.columns.Title.like(search)).join(stock, books.columns.ISBN13 == stock.columns.ISBN13).join(stores, stock.columns.StoreID == stores.columns.ID)

            results = conn.execute(query).fetchall()
        
        # Change format
        for result in results:
            data.append(list(result))
        
        # Update layout
        window['-TABLE-'].update(values=data)
        window[f'-COL{layout}-'].update(visible=False)
        layout = layout + 1 
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'New Search': #update search field with empty string
        window['Input'].update('')
        window[f'-COL{layout}-'].update(visible=False)
        layout = layout -1 
        window[f'-COL{layout}-'].update(visible=True)
        

window.close()














'''
layout1 = [[sg.Text("Welcome to Paige Turner's Bookstore")], 
         [sg.Text("Please enter book title.")], 
         [sg.InputText()], 
         [sg.Submit('submit_button'), sg.Cancel()]]

layout2 = [[sg.Text()]]

window = sg.Window(title="Bookstore", layout=[[layout1]], margins=(300, 150))
'''

'''
# Create an event loop
while True:
    event, values = window.read()

    #inputed_title = input("Enter book title.")

    with engine.connect() as conn: 
        
        metadata = db.MetaData()
        books = db.Table('Books', metadata, autoload=True, autoload_with=engine)
        stock = db.Table('Stock', metadata, autoload=True, autoload_with=engine)
        stores = db.Table('Stores', metadata, autoload=True, autoload_with=engine)

        search = "%{}%".format(values[0])

        query = db.select([books.columns.ISBN13, 
                        books.columns.Title, 
                        stores.columns.Name, 
                        stock.columns.NumberInStock]).filter(books.columns.Title.like(search)).join(stock, books.columns.ISBN13 == stock.columns.ISBN13).join(stores, stock.columns.StoreID == stores.columns.ID)

        ResultProxy = conn.execute(query)
        ResultSet = pd.DataFrame(ResultProxy.fetchall())
    
    #if event == 'submit_button':


    print(ResultSet)
        # End program if user closes window or
        # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()

'''


