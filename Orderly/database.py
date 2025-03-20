# This file will contain the code to connect to the database and create the tables
import sqlite3

def connect():
    conn = sqlite3.connect("orderly.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email unique NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
def get_db_connection():
    conn = sqlite3.connect('orderly.db')
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == '__main__':
    connect()
    print('Tables created')