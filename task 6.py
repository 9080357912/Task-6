#a)
#Setting Up the Database
import sqlite3

def create_tables():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()

    
    c.execute('''CREATE TABLE IF NOT EXISTS PRODUCTS
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 NAME TEXT NOT NULL,
                 PRICE REAL NOT NULL,
                 QUANTITY INTEGER NOT NULL)''')

   
    c.execute('''CREATE TABLE IF NOT EXISTS CUSTOMERS
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 NAME TEXT NOT NULL,
                 EMAIL TEXT NOT NULL)''')

   
    c.execute('''CREATE TABLE IF NOT EXISTS TRANSACTIONS
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 PRODUCT_ID INTEGER NOT NULL,
                 CUSTOMER_ID INTEGER NOT NULL,
                 QUANTITY INTEGER NOT NULL,
                 TOTAL REAL NOT NULL,
                 DATE TEXT NOT NULL,
                 FOREIGN KEY(PRODUCT_ID) REFERENCES PRODUCTS(ID),
                 FOREIGN KEY(CUSTOMER_ID) REFERENCES CUSTOMERS(ID))''')

    conn.commit()
    conn.close()

create_tables()

#b)
# Designi database
import tkinter as tk
from tkinter import messagebox
import sqlite3

def add_product(name, price, quantity):
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute("INSERT INTO PRODUCTS (NAME, PRICE, QUANTITY) VALUES (?, ?, ?)", (name, price, quantity))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Product added successfully")

def add_customer(name, email):
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute("INSERT INTO CUSTOMERS (NAME, EMAIL) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Customer added successfully")

def create_gui():
    root = tk.Tk()
    root.title("Store Management System")

    tk.Label(root, text="Product Name").grid(row=0)
    tk.Label(root, text="Price").grid(row=1)
    tk.Label(root, text="Quantity").grid(row=2)

    product_name = tk.Entry(root)
    price = tk.Entry(root)
    quantity = tk.Entry(root)

    product_name.grid(row=0, column=1)
    price.grid(row=1, column=1)
    quantity.grid(row=2, column=1)

    tk.Button(root, text='Add Product', command=lambda: add_product(product_name.get(), price.get(), quantity.get())).grid(row=3, column=1, sticky=tk.W, pady=4)

    
    tk.Label(root, text="Customer Name").grid(row=4)
    tk.Label(root, text="Email").grid(row=5)

    customer_name = tk.Entry(root)
    email = tk.Entry(root)

    customer_name.grid(row=4, column=1)
    email.grid(row=5, column=1)

    tk.Button(root, text='Add Customer', command=lambda: add_customer(customer_name.get(), email.get())).grid(row=6, column=1, sticky=tk.W, pady=4)

    root.mainloop()

create_gui()



#c)
#GUI Design and Development
def create_invoice(customer_id, product_id, quantity):
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    
    # Fetch product price
    c.execute("SELECT PRICE FROM PRODUCTS WHERE ID = ?", (product_id,))
    price = c.fetchone()[0]
    total = price * int(quantity)
    
    # Create transaction
    c.execute("INSERT INTO TRANSACTIONS (PRODUCT_ID, CUSTOMER_ID, QUANTITY, TOTAL, DATE) VALUES (?, ?, ?, ?, datetime('now'))", 
              (product_id, customer_id, quantity, total))
    
    # Update product quantity
    c.execute("UPDATE PRODUCTS SET QUANTITY = QUANTITY - ? WHERE ID = ?", (quantity, product_id))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Invoice created successfully")

# GUI to create invoice
def create_invoice_gui():
    invoice_window = tk.Toplevel()
    invoice_window.title("Create Invoice")

    tk.Label(invoice_window, text="Customer ID").grid(row=0)
    tk.Label(invoice_window, text="Product ID").grid(row=1)
    tk.Label(invoice_window, text="Quantity").grid(row=2)

    customer_id = tk.Entry(invoice_window)
    product_id = tk.Entry(invoice_window)
    quantity = tk.Entry(invoice_window)

    customer_id.grid(row=0, column=1)
    product_id.grid(row=1, column=1)
    quantity.grid(row=2, column=1)

    tk.Button(invoice_window, text='Create Invoice', command=lambda: create_invoice(customer_id.get(), product_id.get(), quantity.get())).grid(row=3, column=1, sticky=tk.W, pady=4)

create_invoice_gui()


