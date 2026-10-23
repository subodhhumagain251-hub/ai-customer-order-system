
import json 


def load_orders(file_Name):
    try:
        with open(file_Name,"r")as file:
            return json.load(file)
    except FileNotFoundError:
        return[]


def save_orders(filename,orders):
    with open(filename,"w") as file:
        json.dump(orders,file,indent=4)

def calculate_metrics(orders):
    total_items_sold=0
    total_revenue=0
    for order in orders:
        total_items_sold+=order["quantity"]
        total_revenue+= order["quantity"]*order["price"]
    return{"total_items_sold": total_items_sold, "total_revenue": total_revenue}

def add_orders (orders,customer,product,quantity,price):
    if quantity <= 0:
        print("ERROR: Quantity must be greater than 0")
        return orders
    if price <=0:
        print("ERROR: Price must be greater than 0")
        return orders

    new_id=len(orders)+1
    new_order={
        "order_id":new_id,
        "customer":customer,
        "product":product,
        "quantity":quantity,
        "price":price,
        'status':'PENDING'
    }
    orders.append(new_order)
    return orders



def find_order_by_id(orders,target_id):
    for order in orders:
        if order["order_id"]== target_id:
            return order
    return None


def delete_order_by_id(orders,target_id):
    updated_order=[]
    for order in orders:
        if order["order_id"] != target_id:
            updated_order.append(order)
    return updated_order


def update_order_status(orders,target_id,new_status):
    for order in orders:
        if order["order_id"] == target_id:
            order["status"] = new_status
    return orders
