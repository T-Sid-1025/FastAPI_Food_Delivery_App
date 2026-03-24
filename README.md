# 🍔 QuickBite – Food Delivery Backend (FastAPI)

A backend project built using **FastAPI** that simulates how a real-world food delivery system works — from browsing food items to placing orders.

This project was developed during my **FastAPI Internship (Feb 2026)** and focuses on building clean, structured, and scalable APIs.

---

## 🚀 What This Project Does

QuickBite provides a simple backend system where users can:

* Explore available food items
* Add items to a cart
* Place orders
* Search, filter, and sort menu data
* Navigate large datasets using pagination

The goal was to understand how real applications manage workflows behind the scenes.

---

## 🧩 Features Breakdown

### 🔹 Basic API Setup

* Root endpoint to check API status
* Fetch all menu items
* Fetch a specific item using ID
* View all orders
* Menu summary endpoint

---

### 🔹 Data Validation (Pydantic)

* Structured request bodies using `BaseModel`
* Applied validations like:

  * Minimum length
  * Numeric constraints
* Proper error responses for invalid inputs

---

### 🔹 Reusable Logic (Helper Functions)

* `find_menu_item()` → locate items efficiently
* `calculate_bill()` → compute total cost
* `filter_menu_logic()` → apply filtering rules

---

### 🔹 CRUD Operations

* Add new food items
* Update existing items
* Delete items from the menu

---

### 🔹 Cart & Order Flow

* Add items to cart
* View cart contents
* Remove items from cart
* Checkout → automatically creates an order

---

### 🔹 Advanced Functionalities

* Search menu items
* Sort menu based on price/name
* Pagination for large data
* Search & sort orders
* Combined browsing endpoint

---

## 🔄 How the Flow Works

```text
Select Items → Add to Cart → Review Cart → Checkout → Order Generated
```

---

## 🛠️ Tech Stack Used

* FastAPI
* Python
* Pydantic
* Uvicorn

---

## ▶️ Running the Project Locally

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the server

```bash
uvicorn main:app --reload
```

### Step 3: Open API docs

```
http://127.0.0.1:8000/docs
```

---

## 📸 API Testing

All endpoints were tested, and screenshots are available in the `screenshots/` folder.

They include:

* Requests
* Responses
* Status codes

---

## 📁 Folder Structure

```
fastapi-food-delivery-app/
│
├── main.py
├── requirements.txt
├── README.md
├── screenshots/
```

---

## ⚡ Key Things I Focused On

* Writing clean and readable API code
* Proper route structuring
* Handling errors using `HTTPException`
* Keeping logic modular and reusable
* Simulating real-world backend workflow

---

## 🎯 What I Learned

* Building REST APIs using FastAPI
* Validating data with Pydantic
* Designing multi-step workflows (Cart → Order)
* Implementing search, sorting, and pagination
* Structuring backend projects professionally

---

## 🙏 Credits

This project was completed during my internship at
**Innomatics Research Labs**

