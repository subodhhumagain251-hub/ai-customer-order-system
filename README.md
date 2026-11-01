# AI Customer Order Automation Backend API

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()

A modular, production-ready Python RESTful API designed to automate customer order workflows for small retail businesses (such as social commerce clothing brands). Built with **FastAPI**, **Pydantic**, and a decoupled business-logic engine.

---

## 📌 Problem Solved
Small and medium-sized social commerce businesses lose hours every day manually tracking customer orders across messaging channels, managing inventory on spreadsheets, and calculating sales reports.

This system provides a reliable, automated backend that:
1. Validates and records incoming customer orders over HTTP.
2. Tracks order lifecycles from `PENDING` to `PAID`, `SHIPPED`, and `DELIVERED`.
3. Protects financial and inventory calculations against corrupted or negative inputs.
4. Generates real-time business financial metrics on demand.

---

## 🚀 Key Features

- **Full CRUD REST API:** Complete suite of endpoints to Create, Read, Update, and Delete customer orders.
- **Strict Data Validation:** Utilizes **Pydantic** schemas and **Guard Clauses** to prevent corrupt data (blocks negative prices, invalid quantities, and missing fields).
- **Decoupled Architecture:** Business logic (`orders_manager.py`) is completely separated from the HTTP delivery layer (`api.py`), ensuring code reusability across APIs, CLI scripts, and future AI agents.
- **Official HTTP Status Standards:** Fully implements standard status codes (`200 OK`, `201 Created`, `404 Not Found`, and `422 Validation Error`).
- **Resilient File Persistence:** Safely persists and restores records from disk in structured JSON format with `try...except` handling for missing files.
- **Interactive Documentation:** Auto-generated **OpenAPI (Swagger UI)** available out of the box for testing.

---

## 🏗️ Architecture & Project Structure

```text
aicustomer/
│
├── orders_manager.py     # Pure business logic & CRUD engine (The Kitchen)
├── api.py                # FastAPI HTTP routing & request validation (The Waiter)
├── main.py               # Standalone execution & testing script
├── orders.json           # Persistent database on disk
├── README.md             # Project documentation
└── .gitignore            # Git configuration

 REST API Endpoints
Method	Endpoint	Description	Status Code
GET	/	Health check & welcome route	200 OK
GET	/orders	Retrieve all customer orders	200 OK
GET	/orders/{order_id}	Fetch a single order by its ID	200 OK / 404 Not Found
GET	/metrics	Calculate total revenue & items sold	200 OK
POST	/orders	Create a new customer order	201 Created / 422 Error
PATCH	/orders/{order_id}/status	Update order status (PAID, SHIPPED)	200 OK / 404 Not Found
DELETE	/orders/{order_id}	Cancel/delete an order record	200 OK / 404 Not Found

Tech Stack
Language: Python 3.13
Web Framework: FastAPI
Data Validation: Pydantic
ASGI Web Server: Uvicorn
Version Control: Git & GitHub

How to Run Locally
1. Clone the repository

git clone https://github.com/subodhhumagain251-hub/ai-customer-order-system.git
cd ai-customer-order-system

2. Set up a Virtual Environment (Optional but Recommended)

python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

3. Install Dependencies
pip install fastapi uvicorn pydantic

4. Start the API Server
uvicorn api:app --reload

 Interactive API Testing (Swagger UI)
FastAPI automatically generates interactive documentation. Once the server is running, open your browser and navigate to:
👉 http://127.0.0.1:8000/docs
You can test every endpoint directly from your browser:
Click on POST /orders 

 "Try it out".
Send an order payload:
code
JSON
{
  "customer": "Ayush",
  "product": "Winter Jacket",
  "quantity": 1,
  "price": 4000
}
Receive the generated order with automated ID assignment and default "PENDING" status.

 Roadmap (Upcoming Milestones)

Stage 1: Modular Python CRUD engine with defensive validation.

Stage 2: REST API with FastAPI, Pydantic, and HTTP status codes.

Stage 3: Migration from flat JSON files to a relational SQL database (SQLite/PostgreSQL) with ACID transactions.

Stage 4: n8n Workflow Automation: Automated webhook listeners for messaging platforms.

Stage 5: AI Integration: Integrating LLM APIs for natural-language order extraction (e.g., extracting product, variant, and quantity from freeform chat messages).

Stage 6: Payment verification (eSewa/Khalti simulation) and automated courier dispatch webhooks.


Author
Subodh Humagain
B.Sc. Computational Mathematics, Kathmandu University (KU), Nepal
GitHub: @subodhhumagain251-hub
Email: subodhhumagain251@gmail.com
Focus: Python Backend Engineering, Workflow Automation, and AI Systems Integration.