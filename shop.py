
import sqlite3
from datetime import datetime
from database import connect


class Shop:

    def add_product(self, name, buy_price, sell_price, quantity):
        '''
        Create a new product
        '''
        conn = connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO products (name, buy_price, sell_price, stock)
                VALUES (?, ?, ?, ?)
            """, (name, buy_price, sell_price, quantity))

            conn.commit()
            return True, "Product added successfully"

        except sqlite3.IntegrityError:
            return False, "Product already exists"

        finally:
            conn.close()

    def add_stock(self, product_id, quantity):
        '''
        Add stock to an existing product
        '''
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE products
            SET stock = stock + ?
            WHERE id = ?
        """, (quantity, product_id))

        conn.commit()
        conn.close()

    def sell_product(self, product_id, quantity):
        '''
        Sell a product
        '''
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT stock, sell_price FROM products WHERE id = ?",
            (product_id,)
        )

        product = cursor.fetchone()

        if not product:
            conn.close()
            return False, "Product not found"

        stock, sell_price = product

        if quantity <= 0:
            conn.close()
            return False, "Invalid quantity"

        if stock < quantity:
            conn.close()
            return False, "Not enough stock"

        cursor.execute("""
            UPDATE products
            SET stock = stock - ?
            WHERE id = ?
        """, (quantity, product_id))

        cursor.execute("""
            INSERT INTO sales (product_id, quantity, unit_price, sale_date)
            VALUES (?, ?, ?, ?)
        """, (product_id, quantity, sell_price, datetime.now().isoformat()))

        conn.commit()
        conn.close()

        return True, "Sale completed successfully"

    def search_product(self, name):
        '''
        Search for a product by name
        '''
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM products
            WHERE name LIKE ?
        """, (f"%{name}%",))

        products = cursor.fetchall()
        conn.close()

        return products

    def get_products(self):
        '''
        Get all products
        '''
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        conn.close()
        return products

    def sales_report(self, start_date, end_date):
        '''
        Generate  report for  date range
        '''
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COALESCE(SUM(quantity), 0),
                COALESCE(SUM(quantity * unit_price), 0)
            FROM sales
            WHERE date(sale_date) BETWEEN ? AND ?
        """, (start_date, end_date))

        report = cursor.fetchone()
        conn.close()

        return report
