from fastapi import FastAPI ,HTTPException,status,Response
from pydantic import BaseModel 
from ai_extractor import extract_order_from_txt 

from database import(

    init_db,
    add_order_to_db,
    create_order_with_inventory,
    get_all_products,
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

class NaturalOrderRequest(BaseModel):
    message:str 

@app.post("/orders/ai", status_code=status.HTTP_201_CREATED)
def create_ai_order(payload: NaturalOrderRequest, response: Response):
    extracted = extract_order_from_txt(payload.message)
    intent = extracted.get("intent", "INQUIRY")

    if intent != "ORDER" or not extracted.get("product"):
        response.status_code = status.HTTP_200_OK
        products = get_all_products()
        in_stock = [f"{p['name']} (Rs. {p['price']})" for p in products if p["stock"] > 0]
        return {
            "status": "clarification_needed",
            "intent": intent,
            "reply": f"Hi! Here is what we currently have in stock: {', '.join(in_stock)}. Which item and quantity would you like to order?",
        }

    result = create_order_with_inventory(
        extracted["customer"],
        extracted["product"],
        extracted["quantity"],
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "status": "order_created",
        "message": "AI order created successfully!",
        "reply": f"Thank you {result['customer']}! Order #{result['order_id']} for {result['quantity']}x {result['product']} is confirmed. Total: Rs. {result['total_price']}.",
        "order": result,
    }
    
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
        raise HTTPException (status_code=404,detail="Order not found")
    return {"message": "Order status updated successfully in database!",
            "order_id":order_id,
            "new_status": update_data.status }

@app.delete("/orders/{order_id}")
def cancel_order(order_id: int):
    deleted = delete_order(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": f"Order {order_id} has been deleted successfully from database!"}