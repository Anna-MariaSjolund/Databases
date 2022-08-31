import sqlalchemy as db

def create_tables(engine:db.engine):
    """
    Creates and returns metadata tables.
    """
    
    metadata = db.MetaData()
    authors = db.Table('Authors', metadata, autoload=True, autoload_with=engine)     
    books = db.Table('Books', metadata, autoload=True, autoload_with=engine)
    authors2books = db.Table('Authors2Books', metadata, autoload=True, autoload_with=engine) 
    stores = db.Table('Stores', metadata, autoload=True, autoload_with=engine)          
    stock = db.Table('Stock', metadata, autoload=True, autoload_with=engine)

    return authors, books, authors2books, stores, stock