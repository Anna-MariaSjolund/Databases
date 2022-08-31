import PySimpleGUI as sg
from database_connect import db_connect
from queries import search_book, stock_info

# CONNECTION

engine = db_connect("localhost", "bookstore", "bookstoreUser", "veryStrongPassword6293042")

# LAYOUTS

book_data = []
stock_data = []
book_headings = ['ISBN13', 'Title', 'Author']
stock_headings = ['Store Name', 'City', 'Number in Stock']

layout1 = [[sg.Text("Welcome to Paige Turner's Bookstore!", font=('Avenir Next', 30))],
          [sg.Text("Please enter the book title:", font=('Avenir', 15))],
          [sg.InputText(key='-INPUT-', font=('Avenir', 15), size=50)], 
          [sg.Submit('Submit', font=('Avenir', 12)), sg.Button('Exit', key='Exit1', font=('Avenir', 12))]]

layout2 = [[sg.Text('Found the following results (click on item for stock info):', font=('Avenir', 15))],
          [sg.Table(key='-TABLE1-', values=book_data, headings=book_headings, font=('Avenir', 12), justification='c', col_widths = [15, 30, 15], auto_size_columns=False,  enable_events=True)], 
          [sg.Table(key='-TABLE2-', values=stock_data, headings=stock_headings, font=('Avenir', 12), justification='c', col_widths = [30, 15, 15], auto_size_columns=False, num_rows=3, hide_vertical_scroll=True)], 
          [sg.Button('New Search', key='Search1', font=('Avenir', 12)), sg.Button('Exit', key='Exit2', font=('Avenir', 12))]]

layout3 = [[sg.Text('Your search did not match any titles. Please try again or exit.', font=('Avenir', 15))],
          [sg.Button('New Search', key='Search2', font=('Avenir', 12)), sg.Button('Exit', key='Exit3', font=('Avenir', 12))]]

layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), sg.Column(layout3, visible=False, key='-COL3-')]]

#WINDOW

window = sg.Window('Bookstore Search', layout, keep_on_top=True, element_justification='c')

#INITIAL LAYOUT

layout = 1 

#EVENT LOOP

while True:

    event, values = window.read()
    print(event, values)

    if event in (None, 'Exit1', 'Exit2', 'Exit3'):
        break

    if event == '-TABLE1-':
        if len(values['-TABLE1-']) != 0:
            stock_data = stock_info(engine, values['-TABLE1-'][0], book_data)
            window['-TABLE2-'].update(values=stock_data)
        else:
            window['-TABLE2-'].update(values=['', ''])
            
    if event == 'Submit':
        book_data = search_book(engine, values['-INPUT-'])
        if len(book_data) == 0:
            window[f'-COL{layout}-'].update(visible=False)
            layout = layout + 2 
            window[f'-COL{layout}-'].update(visible=True)           
        else:
            window['-TABLE1-'].update(values=book_data)
            window[f'-COL{layout}-'].update(visible=False)
            layout = layout + 1 
            window[f'-COL{layout}-'].update(visible=True)

    if event in ('Search1', 'Search2'): 
        window['-INPUT-'].update('')
        window[f'-COL{layout}-'].update(visible=False)
        layout = 1
        window[f'-COL1-'].update(visible=True)
        
window.close()