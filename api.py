from fastapi import FastAPI ,HTTPException,status
from pydantic import BaseModel 
from database import(

    init_db,
    add_order_to_db,
    create_order_with_inventory,
    get_all_orders,
    get_order_by_id,
    update_order_status,
    delete_order, 
    calculate_metrics_from_db


)

app =FastAPI()


init_db()

class OrderCreate(BaseModel):
    customer:str
    product:str
    quantity :int
    

class StatusUpdate(BaseModel):
    status:str 


@app.get("/orders")
def get_orders():
    return get_all_orders()


@app.get("/metrics")
def get_metrics():
    return calculate_metrics_from_db()

@app.get("/orders/{order_id}")

def get_order(order_id: int):
    found= get_order_by_id(order_id)
    if found is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found ")
    return found 




@app.post("/orders",status_code=status.HTTP_201_CREATED)
def create_order(new_order: OrderCreate):
    if new_order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity and price must be greater than 0 ")
 
    result= create_order_with_inventory(
            new_order.customer,
            new_order.product,
            new_order.quantity,
    )
    print("DEBUG WHAT IS RESULT:",result)
    
    if result["success"]==False:
        raise HTTPException(status_code=400,detail=result["error"])
    
    return {"message": "Order created successfully in SQL database!" , "order":result}

@app.patch("/orders/{order_id}/status")
def change_order_status(order_id: int ,update_data:StatusUpdate):
    updated =update_order_status(order_id,update_data.status)
    if not updated:
        raise HTTPException (status_code=400,detail="Order not found")
    return {"message": "Order status updated successfully in database!",
            "order_id":order_id,
            "new_status": update_data.status }

@app.delete("/orders/{order_id}")
def cancel_order(order_id: int):
    deleted = delete_order(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": f"Order {order_id} has been deleted successfully from database!"}