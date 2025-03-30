import tkinter
from tkinter import ttk
import numpy as np
import pymysql
from datetime import datetime
import csv
import random
from tkinter import *
from tkinter import messagebox




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
        my_tree.insert(parent='', index='end', iid=str(array[0]), text="", values=(array), tag="orow")
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

def save_data():
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

frame = tkinter.Frame(window, bg='#02577A')
frame.pack()

btnColor = "#196E78"

manageframe = tkinter.LabelFrame(frame, text="Manage", borderwidth=5)
manageframe.grid(row=0, column=0, sticky="w", padx=[10, 200], pady=20, ipadx=[6])

saveBtn = tkinter.Button(manageframe, text="SAVE", width=10, borderwidth=3, bg=btnColor, fg='white', command=save_data)
updateBtn = tkinter.Button(manageframe, text="UPDATE", width=10, borderwidth=3, bg=btnColor, fg='white')
deleteBtn = tkinter.Button(manageframe, text="DELETE", width=10, borderwidth=3, bg=btnColor, fg='white')
selectBtn = tkinter.Button(manageframe, text="SELECT", width=10, borderwidth=3, bg=btnColor, fg='white')
findBtn = tkinter.Button(manageframe, text="FIND", width=10, borderwidth=3, bg=btnColor, fg='white')
clearBtn = tkinter.Button(manageframe, text="CLEAR", width=10, borderwidth=3, bg=btnColor, fg='white')
exportBtn = tkinter.Button(manageframe, text="EXPORT EXCEL", width=10, borderwidth=3, bg=btnColor, fg='white')

saveBtn.grid(row=0, column=0, padx=5, pady=5)
updateBtn.grid(row=0, column=1, padx=5, pady=5)
deleteBtn.grid(row=0, column=2, padx=5, pady=5)
selectBtn.grid(row=0, column=3, padx=5, pady=5)
findBtn.grid(row=0, column=4, padx=5, pady=5)
clearBtn.grid(row=0, column=5, padx=5, pady=5)
exportBtn.grid(row=0, column=6, padx=5, pady=5)


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
my_tree['columns']=("Id", "item Id", "Name", "Price", "Quantity", "Category", "Date")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("item Id", anchor=W, width=70)
my_tree.column("Name", anchor=W, width=125)
my_tree.column("Price", anchor=W, width=125)
my_tree.column("Quantity", anchor=W, width=100)
my_tree.column("Category", anchor=W, width=150)
my_tree.column("Date", anchor=W, width=150)

my_tree.heading("Id", text="Id", anchor=W)
my_tree.heading("item Id", text="Item Id", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Price", text="Price", anchor=W)
my_tree.heading("Quantity", text="Quantity", anchor=W)
my_tree.heading("Category", text="Category", anchor=W)
my_tree.heading("Date", text="Date", anchor=W)

my_tree.tag_configure('orrow', background="#EEEEEE")
my_tree.pack()


window.resizable(True, False)
window.mainloop()