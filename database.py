import sqlite3


def init_db():
    conn=sqlite3.connect("orders.db")
    cursor=conn.cursor()
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS orders(
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer TEXT NOT NULL,
        product TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        PRICE REAL NOT NULL,
        status  TEXT DEFAULT 'PENDING '
        )




""")

    conn.commit()
    conn.close()
    print("Databse and 'orders' table initalized sucessfully")



def add_order_to_db(customer,product,quantity,price):
    conn=sqlite3.connect("orders.db")
    cursor=conn.cursor()
    cursor.execute(""" 
        INSERT INTO orders(customer, product, quantity, price)
        VALUES(?,?,?,?)

    """,(customer,product,quantity,price))
    conn.commit()
    conn.close()


def get_all_orders():
    conn=sqlite3.connect("orders.db")
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()

    cursor.execute("select * FROM orders")
    rows=cursor.fetchall()
    conn.close()

    orders_list =[]
    for row in rows:
        orders_list.append(dict(row))

    return orders_list
def get_order_by_id(order_id):
    conn=sqlite3.connect("orders.db")
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id=? ",(order_id,)) 

    row = cursor.fetchone()
    conn.close 

    if row is None:
        return None
    return dict(row)

def update_order_status(order_id,new_status):
    conn=sqlite3.connect("orders.db")
    cursor=conn.cursor()
    #upadte status of the id we gave 
    cursor.execute("UPDATE orders SET status=? WHERE order_id =?",(new_status,order_id))
    #any change db required commit 
    conn.commit()
    conn.close()

#cursor.rowcount how many rows were changed
    rows_affected =cursor.rowcount 
    conn.close()
#return True if orders was updated ,false not exist 
    return rows_affected > 0

def delete_order(order_id):
    conn=sqlite3.connect("orders.db") 
    cursor=conn.cursor()
    cursor.execute("DELETE FROM orders WHERE order_id =?",(order_id,))

    conn.commit()
    rows_affected = cursor.rowcount 
    conn.close()
    return rows_affected > 0

if __name__ == "__main__":
    init_db()

    print("\n 1. INSERTING ORDER ")
    add_order_to_db("Amy", "Winter Hoodie", 2, 2050.0)

    print("\n  2. READING ALL ORDERS ")
    orders = get_all_orders()
    for o in orders:
        print(o)

    # Grab the ID of the order we just created:
    latest_id = orders[-1]["order_id"]

    print(f"\n 3. UPDATING ORDER {latest_id} TO 'PAID' ")
    update_order_status(latest_id, "PAID")
    print(get_order_by_id(latest_id))

    print(f"\n 4. DELETING ORDER {latest_id} ")
    delete_order(latest_id)
    print("Does it still exist?", get_order_by_id(latest_id))