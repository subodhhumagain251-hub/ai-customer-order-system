import sqlite3
def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            status TEXT DEFAULT 'PENDING'
        )
    """)


    #2 products table 
    cursor.execute(""" CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    name TEXT NOT NULL UNIQUE,
    price REAL NOT NULL,
    stock INTEGER NOT NULL )""")

    cursor.execute("SELECT COUNT (*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(""" INSERT INTO products (name,price,stock)
                            VALUES(?,?,?)"""
                           ,[("Black Hoodie",2500.0,10),
                             ("White T-Shirt",800.0,25),
                             ("Casual Cap",500.0,15)
                             ])
    conn.commit()
    conn.close()
    print("Database and 'orders' table initialized successfully")

def get_all_products():
    conn =sqlite3.connect("orders.db")
    conn.row_factory=sqlite3.Row
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows=cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows ]


def add_order_to_db(customer, product, quantity, price):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO orders (customer, product, quantity, price)
        VALUES (?, ?, ?, ?)
    """, (customer, product, quantity, price))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def create_order_with_inventory(customer,product_name,quantity):
    conn=sqlite3.connect("orders.db")
    conn.row_factory=sqlite3.Row
    cursor= conn.cursor()


    cursor.execute("SELECT * FROM products WHERE name = ? COLLATE NOCASE",
                   (product_name,))
    product=cursor.fetchone()

    if product is None:
        conn.close()
        return{"Sucess": False,"error":"Product not found in store catalog"}

    if product["stock"] < quantity:
        conn.close()
        return{"success": False, "error": f"Insufficient stock! Only {product['stock']} available."}
    new_stock= product["stock"]-quantity
    cursor.execute("UPDATE products SET stock =? WHERE product_id=?",
                   (new_stock,product["product_id"]))
    official_price=product["price"]
    cursor.execute(""" 
        INSERT INTO orders(customer,product,quantity,price ,status)
        VALUES(?,?,?,?,"PENDING")""",
        (customer,product["name"],quantity,official_price))
    order_id= cursor.lastrowid
    conn.commit()
    conn.close()
    return {
        "success": True,
        "order_id": order_id,
        "customer": customer,
        "product": product["name"],
        "quantity": quantity,
        "unit_price": official_price,
        "total_price": quantity * official_price,
        "remaining_stock": new_stock
    }

def get_all_orders():
    conn = sqlite3.connect("orders.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    conn.close()

    orders_list = []
    for row in rows:
        orders_list.append(dict(row))

    return orders_list


def get_order_by_id(order_id):
    conn = sqlite3.connect("orders.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)) 
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None
    return dict(row)


def update_order_status(order_id, new_status):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (new_status, order_id))
    conn.commit()
    rows_affected = cursor.rowcount 
    conn.close()
    return rows_affected > 0


def delete_order(order_id):
    conn = sqlite3.connect("orders.db") 
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
    conn.commit()
    rows_affected = cursor.rowcount 
    conn.close()
    return rows_affected > 0


def calculate_metrics_from_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("""  
        SELECT 
            COALESCE(SUM(quantity), 0) AS total_items_sold,
            COALESCE(SUM(quantity * price), 0) AS total_revenue
        FROM orders
    """)
    row = cursor.fetchone()
    conn.close()

    return {
        "total_items_sold": row[0],
        "total_revenue": row[1]
    }


if __name__ == "__main__":
    init_db()


    print("\n1. INSERTING ORDER")
    latest_id = add_order_to_db("Amy", "Winter Hoodie", 2, 2050.0)

    print("\n2. READING ALL ORDERS")
    orders = get_all_orders()
    for o in orders:
        print(o)

    print(f"\n3. UPDATING ORDER {latest_id} TO 'PAID'")
    update_order_status(latest_id, "PAID")
    print(get_order_by_id(latest_id))

    print(f"\n4. DELETING ORDER {latest_id}")
    delete_order(latest_id)
    print("Does it still exist?", get_order_by_id(latest_id))


    
