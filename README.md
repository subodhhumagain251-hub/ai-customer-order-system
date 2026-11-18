# AI Customer Order Automation Backend API

A modular, event-driven Python backend that automates customer order
workflows for small retail and social-commerce businesses.

Built using **FastAPI**, **Pydantic**, **SQLite**, **Groq LLM**, and
**n8n**, this system processes natural-language customer messages,
identifies ordering intent, validates products against a live inventory
catalog, deducts stock atomically, and generates structured order
confirmations.

------------------------------------------------------------------------

## Problem Statement

Small retail businesses and social-commerce brands often spend hours
manually managing customer orders. Common challenges include:

-   Reading and interpreting unstructured customer messages.
-   Checking product availability and calculating prices manually.
-   Updating inventory and tracking order statuses.
-   Managing order records across different platforms.
-   Calculating total sales, revenue, and inventory metrics.

This project addresses these challenges by automating the complete
order-processing workflow, from receiving a customer message to
confirming the order and updating the database.

------------------------------------------------------------------------

## Features

### 1. AI-Powered Natural Language Ordering

**Endpoint:** `POST /orders/ai`

-   Uses Groq LLM with structured JSON output
    (`response_format={"type": "json_object"}`).
-   Extracts `intent`, `customer`, `product`, and `quantity` from
    natural-language messages.
-   Handles common spelling mistakes, plurals, and variations in product
    names.
-   Grounds extracted products against the live SQLite catalog.
-   Uses official database pricing instead of AI-generated prices.

### 2. Intent Classification & Ambiguity Handling

The AI extractor identifies three message types:

  -----------------------------------------------------------------------
  Intent                              Behavior
  ----------------------------------- -----------------------------------
  `ORDER`                             Validates the request, checks
                                      stock, and processes the order
                                      (`201 Created`).

  `INQUIRY`                           Returns relevant in-stock product
                                      and price information (`200 OK`)
                                      without touching inventory.

  `INCOMPLETE`                        Requests clarification when
                                      essential information, such as the
                                      product name, is missing
                                      (`200 OK`).
  -----------------------------------------------------------------------

This prevents casual product inquiries from accidentally creating orders
or modifying inventory.

### 3. Atomic Inventory Management

-   Checks product availability before confirming an order.
-   Deducts stock using a conditional SQL update
    (`WHERE product_id = ? AND stock >= ?`).
-   Uses SQLite transactions to maintain data consistency and prevent
    negative stock.
-   Uses official catalog prices (`quantity * official_price`) for order
    calculations.

### 4. Full CRUD Order Management

Supports standard REST operations with Pydantic validation and HTTP
status codes (`200`, `201`, `400`, `404`, `422`):

-   Create customer orders.
-   Retrieve individual orders or list all orders.
-   Update order status (`PENDING`, `PAID`, `SHIPPED`, `DELIVERED`).
-   Delete orders.

### 5. n8n Workflow Integration

Automates communication between customer messaging platforms and the
backend:

``` text
Customer Message
       |
       v
  n8n Webhook
       |
       v
 HTTP Request (POST /orders/ai)
       |
       v
 FastAPI Backend
       |
       v
 AI Processing
       |
       v
 SQLite Database
       |
       v
 Order Confirmation
```

n8n handles webhook triggers, HTTP requests, and automated customer
responses through the **Respond to Webhook** node.

### 6. Business Metrics

**Endpoint:** `GET /metrics`

Provides real-time business statistics using SQL aggregation (`SUM()`
and `COALESCE()`):

-   Total items sold.
-   Total revenue.

### 7. Interactive API Documentation

FastAPI automatically generates interactive Swagger documentation at:

`http://127.0.0.1:8000/docs`

------------------------------------------------------------------------

## Tech Stack

  Technology          Purpose
  ------------------- -------------------------------------------------------
  Python 3.13         Backend programming
  FastAPI & Uvicorn   REST API framework and ASGI server
  Pydantic            Request validation and data schemas
  SQLite              Product catalog and order database
  Groq LLM            Natural-language processing and intent classification
  python-dotenv       Environment variable and secrets management
  n8n                 Workflow automation and orchestration
  Swagger / OpenAPI   Interactive API documentation

------------------------------------------------------------------------

## Project Structure

``` text
ai-customer-order-system/
│
├── api.py                # FastAPI routes, Pydantic schemas & AI order branching
├── ai_extractor.py       # Groq LLM extraction & catalog grounding
├── database.py           # SQLite schema and atomic transactions
├── orders_manager.py     # Standalone JSON CRUD engine (legacy Stage 1)
├── main.py               # Standalone CLI execution and testing
├── requirements.txt      # Python dependencies
├── .gitignore            # Excludes .env, *.db, .venv, and temporary files
└── README.md             # Project documentation
```

------------------------------------------------------------------------

## Installation & Setup

### 1. Clone the Repository

``` bash
git clone https://github.com/subodhhumagain251-hub/ai-customer-order-system.git
cd ai-customer-order-system
```

### 2. Create and Activate a Virtual Environment

Create the environment:

``` bash
python -m venv .venv
```

**Windows (PowerShell):**

``` powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

``` bash
source .venv/bin/activate
```

### 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

``` env
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder with your actual Groq API key.

**Important:** Never commit your `.env` file or expose your API key
publicly. Make sure `.env` is listed in `.gitignore`.

### 5. Start the FastAPI Server

``` bash
uvicorn api:app --reload
```

The API base URL is:

`http://127.0.0.1:8000`

Swagger documentation:

`http://127.0.0.1:8000/docs`

------------------------------------------------------------------------

## API Endpoints

  Method     Endpoint                      Description
  ---------- ----------------------------- --------------------------------------------
  `POST`     `/orders/ai`                  Process natural-language customer messages
  `POST`     `/orders`                     Create a new order with structured JSON
  `GET`      `/orders`                     Retrieve all orders
  `GET`      `/orders/{order_id}`          Retrieve a specific order
  `PATCH`    `/orders/{order_id}/status`   Update an order's status
  `DELETE`   `/orders/{order_id}`          Delete an order
  `GET`      `/metrics`                    Retrieve sales and revenue metrics

------------------------------------------------------------------------

## Example: AI-Powered Order Processing

### Customer Message

> Hi, I want to buy 2 Black Hoodies please. My name is Rahul.

### API Request

**Method:** `POST`\
**Endpoint:** `/orders/ai`

``` json
{
  "message": "Hi, I want to buy 2 Black Hoodies please. My name is Rahul."
}
```

### Processing Flow

1.  The message is sent to the FastAPI backend.
2.  Groq LLM extracts the customer's intent (`ORDER`) and order details.
3.  The extracted product is matched against the SQLite catalog (for
    example, `Black Hoodie`).
4.  The backend validates the requested quantity against available
    stock.
5.  The official catalog price is retrieved.
6.  Inventory is deducted within an atomic SQLite transaction.
7.  The order is saved and a structured confirmation is returned.

------------------------------------------------------------------------

## Inventory Consistency

A key design decision in this project is using conditional SQL updates
to prevent overselling.

Example:

``` sql
UPDATE products
SET stock = stock - ?
WHERE product_id = ?
  AND stock >= ?;
```

This ensures stock is deducted only when sufficient inventory is
available. The conditional update, combined with transaction handling,
helps prevent negative stock when multiple orders are processed.

------------------------------------------------------------------------

## n8n Workflow Automation

The system uses n8n to connect incoming customer messages with the
backend API.

``` text
Customer Message
       |
       v
  n8n Webhook
       |
       v
 HTTP Request (POST /orders/ai)
       |
       v
 FastAPI Backend
       |
       v
 Groq LLM (Intent & Entity Extraction)
       |
       v
 SQLite Database
 (Catalog Validation & Atomic Deduction)
       |
       v
 Respond to Webhook
       |
       v
 Customer Confirmation
```

This workflow separates message orchestration from the backend's core
order-processing logic.

------------------------------------------------------------------------

## Future Improvements

-   Simulated eSewa / Khalti payment verification (`PENDING` → `PAID`).
-   Automated downloadable PDF/TXT order receipts.
-   Profit/loss and remaining-stock analytics dashboard.
-   WhatsApp Business and Telegram bot integration.
-   Multi-product orders and shopping carts.
-   Cloud deployment (Render / Railway) and Docker packaging.

------------------------------------------------------------------------

## Author

**Subodh Humagain**\
B.Sc. Computational Mathematics --- Kathmandu University (KU), Nepal\
GitHub:
[@subodhhumagain251-hub](https://github.com/subodhhumagain251-hub)

**Technologies:** Python · FastAPI · Pydantic · SQLite · Groq · n8n
