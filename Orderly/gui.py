import tkinter as tk
from tkinter import messagebox
from database import get_db_connection

ORDER_STATUSES = ["Pending", "Shipped", "Delivered", "Cancelled"]

class OrderlyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Orderly - Order & Customer Management")
        self.root.geometry("500x500")
        
        tk.Label(root, text="Orderly Management System", font=("Arial", 16)).pack(pady=10)
        
        tk.Button(root, text="Add Customer", command=self.add_customer_window, width=20, height=2).pack(pady=5)
        tk.Button(root, text="View Customers", command=self.view_customers, width=20, height=2).pack(pady=5)
        tk.Button(root, text="Add Order", command=self.add_order_window, width=20, height=2).pack(pady=5)
        tk.Button(root, text="View Orders", command=self.view_orders, width=20, height=2).pack(pady=5)
        tk.Button(root, text="Edit Customer Order", command=self.edit_order_window, width=20, height=2).pack(pady=5)
        tk.Button(root, text="Change Order Status", command=self.change_status_window, width=20, height=2).pack(pady=5)
        tk.Button(root, text="Exit", command=root.quit, width=20, height=2, bg="red").pack(pady=5)

    def add_customer_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Customer")
        add_window.geometry("400x300")

        tk.Label(add_window, text="Name:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        tk.Label(add_window, text="Email:").pack()
        email_entry = tk.Entry(add_window)
        email_entry.pack()

        tk.Label(add_window, text="Phone:").pack()
        phone_entry = tk.Entry(add_window)
        phone_entry.pack()

        def save_customer():
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()

            if not name or not email:
                messagebox.showerror("Error", "Name and Email are required!")
                return

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
                conn.commit()
                messagebox.showinfo("Success", "Customer added successfully!")
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add customer: {e}")
            finally:
                conn.close()

        tk.Button(add_window, text="Save Customer", command=save_customer).pack(pady=10)

    def view_customers(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, phone FROM customers")
        customers = cursor.fetchall()
        conn.close()

        view_window = tk.Toplevel(self.root)
        view_window.title("Customers List")
        view_window.geometry("400x300")

        tk.Label(view_window, text="Customer List", font=("Arial", 14)).pack(pady=5)

        if not customers:
            tk.Label(view_window, text="No customers found.").pack()
        else:
            for customer in customers:
                tk.Label(view_window, text=f"{customer[0]} - {customer[1]}, {customer[2]}, {customer[3]}").pack()

    def add_order_window(self):
        order_window = tk.Toplevel(self.root)
        order_window.title("Add New Order")
        order_window.geometry("400x400")

        tk.Label(order_window, text="Customer ID:").pack()
        customer_id_entry = tk.Entry(order_window)
        customer_id_entry.pack()

        tk.Label(order_window, text="Product Name:").pack()
        product_entry = tk.Entry(order_window)
        product_entry.pack()

        tk.Label(order_window, text="Quantity:").pack()
        quantity_entry = tk.Entry(order_window)
        quantity_entry.pack()

        tk.Label(order_window, text="Price:").pack()
        price_entry = tk.Entry(order_window)
        price_entry.pack()

        tk.Label(order_window, text="Status:").pack()
        status_var = tk.StringVar(order_window)
        status_var.set("Pending")
        tk.OptionMenu(order_window, status_var, *ORDER_STATUSES).pack()

        def save_order():
            try:
                customer_id = int(customer_id_entry.get())
                product = product_entry.get()
                quantity = int(quantity_entry.get())
                price = float(price_entry.get())
                status = status_var.get()

                if not product:
                    messagebox.showerror("Error", "Product name is required!")
                    return

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO orders (customer_id, product, quantity, price, status) VALUES (?, ?, ?, ?, ?)", (customer_id, product, quantity, price, status))
                conn.commit()
                messagebox.showinfo("Success", "Order added successfully!")
                order_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for customer ID, quantity, and price.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add order: {e}")
            finally:
                conn.close()

        tk.Button(order_window, text="Save Order", command=save_order).pack(pady=10)

    def view_orders(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT orders.id, customers.name, orders.product, orders.quantity, orders.price, orders.order_date, orders.status
            FROM orders
            JOIN customers ON orders.customer_id = customers.id
        """)
        orders = cursor.fetchall()
        conn.close()

        view_window = tk.Toplevel(self.root)
        view_window.title("Orders List")
        view_window.geometry("650x400")

        tk.Label(view_window, text="Orders List", font=("Arial", 14)).pack(pady=5)

        if not orders:
            tk.Label(view_window, text="No orders found.").pack()
        else:
            for order in orders:
                tk.Label(view_window, text=f"{order[0]} - {order[1]} | {order[2]} | Qty: {order[3]} | ${order[4]:.2f} | {order[5]} | Status: {order[6]}").pack()

    def edit_order_window(self):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit or Delete Order")
        edit_window.geometry("400x400")

        tk.Label(edit_window, text="Order ID:").pack()
        order_id_entry = tk.Entry(edit_window)
        order_id_entry.pack()

        tk.Label(edit_window, text="New Product Name:").pack()
        product_entry = tk.Entry(edit_window)
        product_entry.pack()

        tk.Label(edit_window, text="New Quantity:").pack()
        quantity_entry = tk.Entry(edit_window)
        quantity_entry.pack()

        tk.Label(edit_window, text="New Price:").pack()
        price_entry = tk.Entry(edit_window)
        price_entry.pack()

        def update_order():
            try:
                order_id = int(order_id_entry.get())
                product = product_entry.get()
                quantity = int(quantity_entry.get())
                price = float(price_entry.get())

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE orders SET product = ?, quantity = ?, price = ? WHERE id = ?", (product, quantity, price, order_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Order updated successfully!")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update order: {e}")

        def delete_order():
            try:
                order_id = int(order_id_entry.get())
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Deleted", "Order deleted successfully!")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete order: {e}")

        tk.Button(edit_window, text="Update Order", command=update_order).pack(pady=5)
        tk.Button(edit_window, text="Delete Order", command=delete_order, bg="red", fg="white").pack(pady=5)

    def change_status_window(self):
        status_window = tk.Toplevel(self.root)
        status_window.title("Change Order Status")
        status_window.geometry("300x250")

        tk.Label(status_window, text="Order ID:").pack()
        order_id_entry = tk.Entry(status_window)
        order_id_entry.pack()

        tk.Label(status_window, text="New Status:").pack()
        status_var = tk.StringVar(status_window)
        status_var.set(ORDER_STATUSES[0])
        tk.OptionMenu(status_window, status_var, *ORDER_STATUSES).pack()

        def update_status():
            try:
                order_id = int(order_id_entry.get())
                new_status = status_var.get()

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Order status updated!")
                status_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update status: {e}")

        tk.Button(status_window, text="Update Status", command=update_status).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderlyApp(root)
    root.mainloop()
