from orders_manager import(
    load_orders,
    save_orders,
    calculate_metrics,
    add_orders,
    find_order_by_id,
    delete_order_by_id,
    update_order_status,

)

 #RUNNING THE STORE 

#load data
orders=load_orders("orders.json")
print("Exisitng orders loaded:",len(orders))

#add an order
orders=add_orders(orders,"suman","jacket",1,3500)

#update status
orders=update_order_status(orders,3,"PAID")

#generate report
report= calculate_metrics(orders)
print("store Report:",report)

#save everything to disk 
save_orders("orders.json",orders) 