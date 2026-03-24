from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()


class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = Field("delivery")


class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True


class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=10)


def find_menu_item(item_id: int):
    for item in menu_items:
        if item["id"] == item_id:
            return item
    return None


def calculate_bill(price: float, quantity: int, order_type: str = "delivery"):
    base = price * quantity
    delivery_charge = 30 if order_type == "delivery" else 0
    return round(base + delivery_charge, 2)


def filter_menu_logic(category: str = None, max_price: float = None, is_available: bool = None):
    filtered = menu_items.copy()
    if category is not None:
        filtered = [item for item in filtered if item["category"].lower() == category.lower()]
    if max_price is not None:
        filtered = [item for item in filtered if item["price"] <= max_price]
    if is_available is not None:
        filtered = [item for item in filtered if item["is_available"] == is_available]
    return filtered


menu_items = [
    {"id": 1, "name": "Margherita Pizza", "price": 8.99, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Veggie Burger", "price": 6.49, "category": "Burgers", "is_available": True},
    {"id": 3, "name": "Caesar Salad", "price": 5.99, "category": "Salads", "is_available": True},
    {"id": 4, "name": "Chicken Wings", "price": 7.99, "category": "Appetizers", "is_available": False},
    {"id": 5, "name": "Chocolate Brownie", "price": 3.99, "category": "Dessert", "is_available": True},
]

orders = [
    {"order_id": 1, "item_id": 1, "quantity": 2, "total_price": 17.98, "status": "pending"},
    {"order_id": 2, "item_id": 3, "quantity": 1, "total_price": 5.99, "status": "completed"},
]

order_counter = len(orders)
cart = []

@app.get("/")
async def read_root():
    return {"message": "Welcome to QuickBite Food Delivery"}

@app.get("/menu")
async def get_menu():
    return {"total": len(menu_items), "menu": menu_items}


@app.post("/menu", status_code=201)
async def create_menu_item(menu_item: NewMenuItem):
    if any(item["name"].lower() == menu_item.name.lower() for item in menu_items):
        raise HTTPException(status_code=400, detail="Menu item with this name already exists")

    new_id = max((item["id"] for item in menu_items), default=0) + 1
    new_item = {
        "id": new_id,
        "name": menu_item.name,
        "price": menu_item.price,
        "category": menu_item.category,
        "is_available": menu_item.is_available,
    }
    menu_items.append(new_item)
    return new_item


@app.get("/menu/summary")
async def get_menu_summary():
    total_items = len(menu_items)
    available_items = sum(1 for item in menu_items if item["is_available"])
    unavailable_items = total_items - available_items
    categories = sorted({item["category"] for item in menu_items})
    return {
        "total_items": total_items,
        "available_items": available_items,
        "unavailable_items": unavailable_items,
        "categories": categories,
    }
@app.get("/menu/filter")
async def filter_menu(category: str = None, max_price: float = None, is_available: bool = None):
    filtered_items = filter_menu_logic(category=category, max_price=max_price, is_available=is_available)
    return {"count": len(filtered_items), "menu": filtered_items}



@app.get("/menu/search")
async def search_menu(keyword: str):
    query = keyword.strip().lower()
    if not query:
        raise HTTPException(status_code=400, detail="Keyword is required")

    results = [item for item in menu_items if query in item["name"].lower()]
    total_found = len(results)
    if total_found == 0:
        return {"message": "No items found", "total_found": 0}

    return {"total_found": total_found, "items": results}


@app.get("/menu/sort")
async def sort_menu(sort_by: str = "price", order: str = "asc"):
    sort_by = sort_by.lower()
    order = order.lower()
    if sort_by not in {"price", "name"}:
        raise HTTPException(status_code=400, detail="sort_by must be 'price' or 'name'")
    if order not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="order must be 'asc' or 'desc'")

    reverse = order == "desc"
    if sort_by == "price":
        sorted_items = sorted(menu_items, key=lambda x: x["price"], reverse=reverse)
    else:
        sorted_items = sorted(menu_items, key=lambda x: x["name"].lower(), reverse=reverse)

    return {"sort_by": sort_by, "order": order, "items": sorted_items}


@app.get("/menu/page")
async def page_menu(page: int = 1, limit: int = 2):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="page and limit must be >= 1")

    total_items = len(menu_items)
    

    total_pages = (total_items + limit - 1) // limit
    
    if page > total_pages and total_pages != 0:
        return {
        "message": "Page out of range",
        "total_pages": total_pages,
        "items": []
    }
    
    start = (page - 1) * limit
    end = start + limit
    paged_items = menu_items[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "items": paged_items,
    }

@app.get("/menu/browse")
async def browse_menu(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4,
):
    # Validate
    sort_by = sort_by.lower()
    order = order.lower()
    if sort_by not in {"price", "name"}:
        raise HTTPException(status_code=400, detail="sort_by must be 'price' or 'name'")
    if order not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="order must be 'asc' or 'desc'")
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="page and limit must be >= 1")

    # 1. Filter
    filtered = menu_items.copy()
    if keyword:
        search = keyword.strip().lower()
        filtered = [item for item in filtered if search in item["name"].lower()]

    # 2. Sort
    reverse = order == "desc"
    if sort_by == "price":
        filtered = sorted(filtered, key=lambda x: x["price"], reverse=reverse)
    else:
        filtered = sorted(filtered, key=lambda x: x["name"].lower(), reverse=reverse)

    # 3. Paginate
    total_found = len(filtered)
    total_pages = (total_found + limit - 1) // limit
    if page > total_pages and total_pages != 0:
        return {
        "message": "Page out of range",
        "total_pages": total_pages,
        "items": []
    }
    start = (page - 1) * limit
    end = start + limit
    items = filtered[start:end]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "items": items,
    }
@app.get("/menu/{item_id}")
async def get_menu_item(item_id: int):
    for item in menu_items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Menu item not found")

@app.put("/menu/{item_id}")
async def update_menu_item(item_id: int, price: float = None, is_available: bool = None):
    item = find_menu_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    if price is not None:
        if price <= 0:
            raise HTTPException(status_code=400, detail="Price must be greater than 0")
        item["price"] = price

    if is_available is not None:
        item["is_available"] = is_available

    return item


@app.delete("/menu/{item_id}")
async def delete_menu_item(item_id: int):
    item = find_menu_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    menu_items.remove(item)
    return {"message": f"Menu item '{item['name']}' deleted successfully"}


@app.post("/cart/add")
async def add_to_cart(item_id: int, quantity: int = 1):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    menu_item = find_menu_item(item_id)
    if menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    if not menu_item["is_available"]:
        raise HTTPException(status_code=400, detail="Menu item is not available")

    cart_item = next((ci for ci in cart if ci["item_id"] == item_id), None)
    if cart_item is not None:
        cart_item["quantity"] += quantity
        cart_item["subtotal"] = round(cart_item["quantity"] * menu_item["price"], 2)
        return {"message": "Cart updated", "cart_item": cart_item}

    new_cart_item = {
        "item_id": item_id,
        "name": menu_item["name"],
        "price": menu_item["price"],
        "quantity": quantity,
        "subtotal": round(quantity * menu_item["price"], 2),
    }
    cart.append(new_cart_item)
    return {"message": "Added to cart", "cart_item": new_cart_item}


@app.delete("/cart/{item_id}")
async def remove_from_cart(item_id: int):
    cart_item = next((ci for ci in cart if ci["item_id"] == item_id), None)
    if cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart.remove(cart_item)
    return {"message": f"Cart item '{cart_item['name']}' removed successfully"}


@app.get("/cart")
async def get_cart():
    if not cart:
        return {"message": "Cart is empty"}

    grand_total = round(sum(ci["subtotal"] for ci in cart), 2)
    return {"items": cart, "item_count": len(cart), "grand_total": grand_total}


@app.post("/cart/checkout", status_code=201)
async def checkout_cart(checkout_request: CheckoutRequest):
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    global order_counter
    grand_total = 0
    created_orders = []

    for ci in cart:
        menu_item = find_menu_item(ci["item_id"])
        if menu_item is None:
            raise HTTPException(status_code=400, detail=f"Menu item {ci['item_id']} is not available for checkout")

        if not menu_item["is_available"]:
            raise HTTPException(status_code=400, detail=f"Menu item {ci['item_id']} is not available")

        subtotal = ci["subtotal"]
        grand_total += subtotal

        order_counter += 1
        new_order = {
            "order_id": order_counter,
            "customer_name": checkout_request.customer_name,
            "item": menu_item,
            "quantity": ci["quantity"],
            "total_price": subtotal,
            "status": "pending",
            "delivery_address": checkout_request.delivery_address,
        }
        orders.append(new_order)
        created_orders.append(new_order)

    cart.clear()

    return {
        "message": "Order placed successfully",
        "orders_placed": created_orders,
        "grand_total": round(grand_total, 2),
    }


@app.get("/orders")
async def get_orders():
    return {"total_orders": len(orders), "orders": orders}


@app.get("/orders/search")
async def search_orders(customer_name: str):
    query = customer_name.strip().lower()
    if not query:
        raise HTTPException(status_code=400, detail="customer_name is required")

    matched = [o for o in orders if query in o.get("customer_name", "").lower()]
    total_found = len(matched)
    if total_found == 0:
        return {"message": "No orders found", "total_found": 0}

    return {"total_found": total_found, "orders": matched}

@app.get("/orders/sort")
def sort_orders(order: str = "asc"):
    if order not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="Invalid order")

    reverse = order == "desc"
    sorted_orders = sorted(orders, key=lambda x: x["total_price"], reverse=reverse)

    return {
        "order": order,
        "orders": sorted_orders
    }

@app.post("/orders")
async def create_order(order_request: OrderRequest):
    menu_item = find_menu_item(order_request.item_id)
    if menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    if not menu_item["is_available"]:
        raise HTTPException(status_code=400, detail="Menu item is not available")

    total_price = calculate_bill(menu_item["price"], order_request.quantity, order_request.order_type)

    global order_counter
    order_counter += 1

    new_order = {
        "order_id": order_counter,
        "customer_name": order_request.customer_name,
        "item": menu_item,
        "quantity": order_request.quantity,
        "total_price": total_price,
        "status": "pending",
    }

    orders.append(new_order)
    return {
    "message": "Order placed successfully",
    "order": new_order
}

