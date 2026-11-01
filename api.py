from fastapi import FastAPI
from orders_manager import(
    
     load_orders,
     save_orders,
     calculate_metrics,
     find_order_by_id,
     add_orders,
     update_order_status,
     delete_order_by_id
     )
from pydantic import BaseModel



# Name the variable 'app':


app = FastAPI()


class OrderCreate(BaseModel):
    customer : str
    product : str 
    quantity : int
    price : float 

class StatusUpdate(BaseModel):
    status:str


@app.get("/")
def home():
    return {"message": "Welcome to the Customer Order API!"}

@app.get("/orders")
def get_all_orders():
    orders = load_orders("orders.json")
    return orders

@app.get("/subodh")
def greeting():
    return {"greetingd":"Namaste Subodh! I MADE THIS ROUTE MYSELF "} 

@app.get("/metrics")
def get_metrics():
    orders=load_orders("orders.json")
    metrics=calculate_metrics(orders)
    return metrics

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    orders= load_orders("orders.json")
    found = find_order_by_id(orders,order_id)

    if found is None:
        return{"error": "orders not found"}
    else:
        return found

@app.post("/orders")
def create_order(new_order: OrderCreate):
    orders=load_orders("orders.json")

    orders=add_orders(

        orders,

        new_order.customer,
        new_order.product,
        new_order.quantity,
        new_order.price,
      
    )

    save_orders("orders.json",orders)
    return{
        "message":"order created sucessfully!",
        "new_order":orders[-1]

    }


@app.patch("/orders/{order_id}/status")
def chage_order_status(order_id:int ,update_data: StatusUpdate):
    orders=load_orders("orders.json")
    existing_order= find_order_by_id(orders,order_id)
    if existing_order is None:
        return{"error":"order Not found"}

    orders=update_order_status(orders,order_id,update_data.status)
    save_orders("orders.json",orders)

    return{
        "message": "Order status updated successfully!",
        "order_id" :order_id,
        "new_status":update_data.status
    }

@app.delete("/orders/{order_id}")
def cancel_order(order_id:int):
    orders=load_orders("orders.json")

    existing =find_order_by_id(orders,order_id)
    if existing is None:
        return{"error":"order not found"}
    orders=delete_order_by_id(orders,order_id)
    save_orders("orders.json",orders)

    return{"message":f"order {order_id} has been deleted sucessfully!",
           "remaining_Order":len(orders)}
