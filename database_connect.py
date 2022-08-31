from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from urllib.parse import unquote
import pyodbc

def db_connect(server_name:str, database_name:str, user_name:str, password:str):
    """
    Connects to the specified database and returns an engine object.
    """

    connection_string = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server_name};DATABASE={database_name};uid={user_name};pwd={password}"
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
    
    return engine