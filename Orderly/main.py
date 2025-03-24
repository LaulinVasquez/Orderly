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
   
   
def add_order():
    """Function to add a new order to the database."""
    customer_id = input("Enter Customer ID: ")
    product = input("Enter Product Name: ")
    quantity = int(input("Enter Quantity: "))
    price = float(input("Enter Price: "))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO orders (customer_id, product, quantity, price) VALUES (?, ?, ?, ?)", (customer_id, product, quantity, price))
        conn.commit()
        print("Order added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Invalid Customer ID!")
    finally:
        conn.close() 
        
        
def view_orders_by_customer():
    customer_id = input("Enter Customer ID to view their orders: ")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT orders.id, customers.name, orders.product, orders.quantity, orders.price, orders.order_date
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
        WHERE orders.customer_id = ?
    """, (customer_id,))
    orders = cursor.fetchall()
    conn.close()
    
    if orders:
        print(f"\nOrders for Customer ID {customer_id}:")
        print("ID | Customer | Product | Quantity | Price | Order Date")
        print("-" * 80)
        for order in orders:
            print(f"{order[0]} | {order[1]} | {order[2]} | {order[3]} | ${order[4]:.2f} | {order[5]}")
    else:
        print("No orders found for this customer.")
        
def update_order():
    """Function to update an order's product, quantity, or price."""
    order_id = input("Enter Order ID to update: ")
    product = input("Enter new Product Name: ")
    quantity = int(input("Enter new Quantity: "))
    price = float(input("Enter new Price: "))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET product = ?, quantity = ?, price = ? WHERE id = ?", (product, quantity, price, order_id))
    conn.commit()
    conn.close()
    print("Order updated successfully!")

def delete_order():
    """Function to delete an order by ID."""
    order_id = input("Enter Order ID to delete: ")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    print("Order deleted successfully!")
        
def menu():
    while True:
        print('''
        \nOrderly - Order & customer Management System
        1. Add New Customer
        2. Add New Order
        3. View Orders
        4. View Customers
        5. edit customer order
        6. Exit
        ''')
        
        choice = input('\n Enter your choice: ')
        
        if choice == '1':
            add_customer()
        elif choice == '2':
            add_order()
        elif choice == '3':
            view_orders_by_customer()
        elif choice == '4':
            view_customers()
        elif choice == '5':
            print(""""
                  1. update customer order
                  2. delete customer order
                  """)
            choice = input("Enter your choice: ")
            if choice == '1':
                update_order()
            elif choice == '2':
                delete_order()
            else:
                print('Invalid choice')
        elif choice == '6':
            print('Exiting... Goodbye!')
            sys.exit()
            
        
if __name__ == '__main__':
    menu()