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


# Idecided to update the order table to have a column for pending orders
def ensure_status_column():
    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute("PRAGMA table_info(orders)")
    columns = [col[1] for col in cursor.fetchall()]

    if "status" not in columns:
        print("Adding 'status' column to orders table...")
        cursor.execute("ALTER TABLE orders ADD COLUMN status TEXT DEFAULT 'Pending'")
        conn.commit()
        print("✅ 'status' column added.")
    else:
        print("✅ 'status' column already exists.")
    
    conn.close()


ensure_status_column()

if __name__ == '__main__':
    connect()
    print('Tables created')