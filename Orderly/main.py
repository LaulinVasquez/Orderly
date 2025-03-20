# This where menu will be created
import sys
import sqlite3
from database import get_db_connection


def add_customer():
    name = input('Enter customer name: ')
    email = input('Enter customer email: ')
    phone = input('Enter customer phone: ')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)
        ''', (name, email, phone))
        conn.commit()
        print('Customer added successfully')
    except sqlite3.Error as e:
        print(f'Error adding customer: {e}')
    finally:
        conn.close()
    
def view_customers():
    """Function to display all customers from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, created_at FROM customers")
    customers = cursor.fetchall()
    conn.close()
    
    if customers:
        print("\nCustomer List:")
        print("ID | Name | Email | Phone | Created At")
        print("-" * 60)
        for customer in customers:
            print(f"{customer[0]} | {customer[1]} | {customer[2]} | {customer[3]} | {customer[4]}")
    else:
        print("No customers found.")
    
def menu():
    while True:
        print('''
        \nOrderly - Order & customer Management System
        1. Add New Customer
        2. Add New Order
        3. View Orders
        4. View Customers
        5. Exit
        ''')
        
        choice = input('\n Enter your choice: ')
        
        if choice == '1':
            add_customer()
        elif choice == '2':
            print('Add New Order - function comming soon')
        elif choice == '3':
            print('View Orders - function comming soon')
        elif choice == '4':
            view_customers()
        elif choice == '5':
            print('Exiting... Goodbye!')
            sys.exit()
            
        
if __name__ == '__main__':
    menu()