
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import create_tables
from shop import Shop


shop = Shop()


def refresh_products():
    for item in tree.get_children():
        tree.delete(item)

    for product in shop.get_products():
        tree.insert("", tk.END, values=product)


def add_product():
    try:
        name = name_entry.get().strip()
        buy_price = float(buy_entry.get())
        sell_price = float(sell_entry.get())
        quantity = int(stock_entry.get())

        if not name or buy_price < 0 or sell_price < 0 or quantity < 0:
            raise ValueError

        success, message = shop.add_product(
            name, buy_price, sell_price, quantity
        )

        if success:
            messagebox.showinfo("Success", message)
            refresh_products()
        else:
            messagebox.showerror("Error", message)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid values")


def add_stock():
    try:
        product_id = int(product_id_entry.get())
        quantity = int(stock_entry.get())

        if quantity <= 0:
            raise ValueError

        shop.add_stock(product_id, quantity)
        refresh_products()
        messagebox.showinfo("Success", "Stock updated")

    except ValueError:
        messagebox.showerror("Error", "Invalid ID or quantity")


def sell_product():
    try:
        product_id = int(product_id_entry.get())
        quantity = int(sell_quantity_entry.get())

        success, message = shop.sell_product(product_id, quantity)

        if success:
            messagebox.showinfo("Success", message)
            refresh_products()
        else:
            messagebox.showerror("Error", message)

    except ValueError:
        messagebox.showerror("Error", "Invalid input")


def search_product():
    name = search_entry.get().strip()

    for item in tree.get_children():
        tree.delete(item)

    for product in shop.search_product(name):
        tree.insert("", tk.END, values=product)


def show_report():
    try:
        start = start_date_entry.get().strip()
        end = end_date_entry.get().strip()

        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")

        if start > end:
            raise ValueError

        total_quantity, total_revenue = shop.sales_report(start, end)

        messagebox.showinfo(
            "Sales Report",
            f"Total sold: {total_quantity}\n"
            f"Total revenue: {total_revenue:,.0f}"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter dates in YYYY-MM-DD format"
        )


root = tk.Tk()
root.title("Shop Management System")
root.geometry("850x650")

# Product form
form = ttk.LabelFrame(root, text="Add Product", padding=10)
form.pack(fill="x", padx=10, pady=10)

ttk.Label(form, text="Name").grid(row=0, column=0, padx=5)
name_entry = ttk.Entry(form)
name_entry.grid(row=0, column=1, padx=5)

ttk.Label(form, text="Buy Price").grid(row=0, column=2, padx=5)
buy_entry = ttk.Entry(form)
buy_entry.grid(row=0, column=3, padx=5)

ttk.Label(form, text="Sell Price").grid(row=0, column=4, padx=5)
sell_entry = ttk.Entry(form)
sell_entry.grid(row=0, column=5, padx=5)

ttk.Label(form, text="Stock").grid(row=0, column=6, padx=5)
stock_entry = ttk.Entry(form, width=8)
stock_entry.grid(row=0, column=7, padx=5)

ttk.Button(form, text="Add Product", command=add_product).grid(
    row=1, column=0, columnspan=8, pady=10
)

# Stock and sales
actions = ttk.LabelFrame(root, text="Stock / Sales", padding=10)
actions.pack(fill="x", padx=10, pady=5)

ttk.Label(actions, text="Product ID").grid(row=0, column=0, padx=5)
product_id_entry = ttk.Entry(actions, width=10)
product_id_entry.grid(row=0, column=1, padx=5)

ttk.Label(actions, text="Quantity").grid(row=0, column=2, padx=5)
sell_quantity_entry = ttk.Entry(actions, width=10)
sell_quantity_entry.grid(row=0, column=3, padx=5)

ttk.Button(actions, text="Sell", command=sell_product).grid(
    row=0, column=4, padx=10
)

ttk.Button(actions, text="Add Stock", command=add_stock).grid(
    row=0, column=5, padx=10
)

# Search
search_frame = ttk.LabelFrame(root, text="Search Product", padding=10)
search_frame.pack(fill="x", padx=10, pady=5)

search_entry = ttk.Entry(search_frame)
search_entry.pack(side="left", padx=5)

ttk.Button(search_frame, text="Search", command=search_product).pack(side="left")
ttk.Button(search_frame, text="Show All", command=refresh_products).pack(side="left")

# Product table
columns = ("ID", "Name", "Buy Price", "Sell Price", "Stock")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=140)

tree.pack(fill="both", expand=True, padx=10, pady=10)

# Sales report
report = ttk.LabelFrame(root, text="Sales Report", padding=10)
report.pack(fill="x", padx=10, pady=10)

ttk.Label(report, text="Start Date (YYYY-MM-DD)").pack(side="left")
start_date_entry = ttk.Entry(report, width=15)
start_date_entry.pack(side="left", padx=5)

ttk.Label(report, text="End Date").pack(side="left")
end_date_entry = ttk.Entry(report, width=15)
end_date_entry.pack(side="left", padx=5)

ttk.Button(report, text="Generate Report", command=show_report).pack(
    side="left", padx=10
)

create_tables()
refresh_products()

root.mainloop()
