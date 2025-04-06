import tkinter
from tkinter import ttk
import numpy as np
import pymysql
from datetime import datetime
import csv
import random
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd


window = tkinter.Tk()
window.title("Stock Management System")
my_tree = ttk.Treeview(window, show='headings', height=20)
window.geometry('1000x640')
style = ttk.Style()

placeholderArray = ['', '', '', '', '']
numeric = '1234567890'
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'



def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='kenneth',
        db='stockmanagementsystem',
    )
    return conn

conn=connection()
cursor=conn.cursor()

for i in range(0,5):
    placeholderArray[i]=tkinter.StringVar()

def read():
    cursor.connection.ping()
    sql=f"SELECT `id`, `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks ORDER BY `id` DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    for array in read():
        my_tree.insert(parent='', index='end', iid=str(array[0]), text="", values=array[1:], tag="orow")
    my_tree.tag_configure('orow', background="#EEEEEE")
    my_tree.pack()

def setph(word, num):
    for ph in range(0,5):
        if ph == num:
            placeholderArray[ph].set(word)

def generateRand():
    itemId=''
    for i in range(0,3):
        randno = random.randrange(0,(len(numeric)-1))
        itemId = itemId+str(numeric[randno])
    randno = random.randrange(0,(len(alpha)-1))
    itemId = itemId+'-'+str(alpha[randno])
    print("generated: "+itemId)
    item_entry.delete(0, tkinter.END)
    item_entry.insert(0, itemId)

def save():
    conn = connection()
    cursor = conn.cursor()

    item_id = item_entry.get()
    name = name_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()
    category = category_entry.get()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if item_id and name and price and quantity and category:
        sql = "INSERT INTO stocks (item_id, name, price, quantity, category, date) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (item_id, name, price, quantity, category, date))
        conn.commit()
        conn.close()
        refreshTable()
        messagebox.showinfo("Success", "Item saved successfully!")
    else:
        messagebox.showerror("Error", "Please fill all fields.")

conn.close()

def select():
    selected = my_tree.focus()
    if not selected:
        messagebox.showwarning("Select", "Please select a row first.")
        return
    values = my_tree.item(selected, 'values')

    item_entry.delete(0, tkinter.END)
    item_entry.insert(0, values[0])

    name_entry.delete(0, tkinter.END)
    name_entry.insert(0, values[1])

    price_entry.delete(0, tkinter.END)
    price_entry.insert(0, values[2])

    quantity_entry.delete(0, tkinter.END)
    quantity_entry.insert(0, values[3])

    category_entry.set(values[4])

def update():
    conn = connection()
    cursor = conn.cursor()

    item_id = item_entry.get()
    name = name_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()
    category = category_entry.get()

    if item_id and name and price and quantity and category:
        try:
            sql = """UPDATE stocks 
                     SET name=%s, price=%s, quantity=%s, category=%s 
                     WHERE item_id=%s"""
            cursor.execute(sql, (name, price, quantity, category, item_id))
            conn.commit()
            refreshTable()
            messagebox.showinfo("Success", "Item updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update item: {e}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Please fill all fields.")
def delete():
    selected = my_tree.focus()
    if not selected:
        messagebox.showwarning("Delete", "Please select an item to delete.")
        return

    item_id = my_tree.item(selected, 'values')[0]

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this item?")
    if not confirm:
        return

    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM stocks WHERE item_id = %s", (item_id,))
        conn.commit()
        refreshTable()
        messagebox.showinfo("Success", "Item deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting item: {e}")
    finally:
        conn.close()

def find():
    search_id = item_entry.get().strip()
    if not search_id:
        messagebox.showwarning("Find", "Enter an Item ID to search.")
        return

    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT item_id, name, price, quantity, category, date FROM stocks WHERE item_id = %s", (search_id,))
        result = cursor.fetchone()
        if result:
            for data in my_tree.get_children():
                my_tree.delete(data)
            my_tree.insert('', 'end', values=result)
        else:
            messagebox.showinfo("Not Found", "No item found with that ID.")
    except Exception as e:
        messagebox.showerror("Error", f"Error searching: {e}")
    finally:
        conn.close()

def export():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        return

    conn = connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT item_id, name, price, quantity, category, date FROM stocks")
        data = cursor.fetchall()
        columns = ["Item ID", "Name", "Price", "Quantity", "Category", "Date"]
        df = pd.DataFrame(data, columns=columns)
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", "Data exported successfully to Excel!")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed: {e}")
    finally:
        conn.close()

def import_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        return

    try:
        df = pd.read_excel(file_path)
        conn = connection()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO stocks (item_id, name, price, quantity, category, date)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name), price=VALUES(price), quantity=VALUES(quantity), category=VALUES(category), date=VALUES(date)
            """, tuple(row))

        conn.commit()
        refreshTable()
        messagebox.showinfo("Success", "Data imported successfully from Excel!")
    except Exception as e:
        messagebox.showerror("Error", f"Import failed: {e}")
    finally:
        conn.close()

def clear():
    item_entry.delete(0, tkinter.END)
    name_entry.delete(0, tkinter.END)
    price_entry.delete(0, tkinter.END)
    quantity_entry.delete(0, tkinter.END)
    category_entry.set('')


frame = tkinter.Frame(window, bg='#02577A')
frame.pack()

btnColor = "#196E78"

manageframe = tkinter.LabelFrame(frame, text="Manage", borderwidth=5)
manageframe.grid(row=0, column=0, sticky="w", padx=[10, 200], pady=20, ipadx=[6])

saveBtn = tkinter.Button(manageframe, text="SAVE", width=10, borderwidth=3, bg=btnColor, fg='white', command=save)
updateBtn = tkinter.Button(manageframe, text="UPDATE", width=10, borderwidth=3, bg=btnColor, fg='white', command=update)
deleteBtn = tkinter.Button(manageframe, text="DELETE", width=10, borderwidth=3, bg=btnColor, fg='white', command=delete)
selectBtn = tkinter.Button(manageframe, text="SELECT", width=10, borderwidth=3, bg=btnColor, fg='white', command=select)
findBtn = tkinter.Button(manageframe, text="FIND", width=10, borderwidth=3, bg=btnColor, fg='white', command=find)
clearBtn = tkinter.Button(manageframe, text="CLEAR", width=10, borderwidth=3, bg=btnColor, fg='white', command=clear)
exportBtn = tkinter.Button(manageframe, text="EXPORT EXCEL", width=10, borderwidth=3, bg=btnColor, fg='white', command=export)
importBtn = tkinter.Button(manageframe, text="IMPORT EXCEL", width=10, borderwidth=3, bg=btnColor, fg='white', command=import_excel)

saveBtn.grid(row=0, column=0, padx=5, pady=5)
updateBtn.grid(row=0, column=1, padx=5, pady=5)
deleteBtn.grid(row=0, column=2, padx=5, pady=5)
selectBtn.grid(row=0, column=3, padx=5, pady=5)
findBtn.grid(row=0, column=4, padx=5, pady=5)
clearBtn.grid(row=0, column=5, padx=5, pady=5)
exportBtn.grid(row=0, column=6, padx=5, pady=5)
importBtn.grid(row=0, column=7, padx=5, pady=5)


form_label = tkinter.LabelFrame(frame, text="Form", borderwidth=5)
form_label.grid(row=1, column=0, sticky="w", padx=[10, 200], pady=20, ipadx=[6])
item_label = tkinter.Label(form_label, text="ITEM ID")
item_label.grid(row=0, column=0)
item_entry = tkinter.Entry(form_label, width=50)
item_entry.grid(row=0, column=1, pady=10)
butt = tkinter.Button(form_label, text="GENERATE ID", bg=btnColor, fg='white', borderwidth=3, command=generateRand)
butt.grid(row=0, column=2, padx=5, pady=5)
name_label = tkinter.Label(form_label, text='NAME')
name_label.grid(row=1, column=0)
name_entry = tkinter.Entry(form_label, width=50)
name_entry.grid(row=1, column=1, pady=10)
price_label = tkinter.Label(form_label, text="PRICE")
price_label.grid(row=2, column=0)
price_entry = tkinter.Entry(form_label, width=50)
price_entry.grid(row=2, column=1, pady=20)
quantity = tkinter.Label(form_label, text="QNT")
quantity.grid(row=3, column=0)
quantity_entry = tkinter.Entry(form_label, width=50)
quantity_entry.grid(row=3, column=1, pady=10)
category = tkinter.Label(form_label, text="CATEGORY", anchor="e", width=10)
category.grid(row=4, column=0, padx=10)

categoryArray = ["Networking Tools", "Computer Parts", "Repair Tools", "Gadgets"]

category_entry = ttk.Combobox(form_label, values=categoryArray, width=50, textvariable=placeholderArray[4])
category_entry.grid(row=4, column=1, pady=10)


style.configure("Treeview", rowheight=25)
my_tree['columns']=("item Id", "Name", "Price", "Quantity", "Category", "Date")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("item Id", anchor=W, width=70)
my_tree.column("Name", anchor=W, width=125)
my_tree.column("Price", anchor=W, width=125)
my_tree.column("Quantity", anchor=W, width=100)
my_tree.column("Category", anchor=W, width=150)
my_tree.column("Date", anchor=W, width=150)


my_tree.heading("item Id", text="Item Id", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Price", text="Price", anchor=W)
my_tree.heading("Quantity", text="Quantity", anchor=W)
my_tree.heading("Category", text="Category", anchor=W)
my_tree.heading("Date", text="Date", anchor=W)

my_tree.tag_configure('orrow', background="#EEEEEE")
my_tree.pack()

refreshTable()
window.resizable(True, False)
window.mainloop()
