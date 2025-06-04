# AWE Electronics


AWE Electronics is a Flask-based e-commerce web application featuring user and admin roles, product management, and order handling — all powered by simple JSON file storage and vanilla JavaScript frontend.

---
## Features

    - User registration and secure login with hashed passwords  
    - Admin login via secret code (no admin JSON file)  
    - Admin product upload with image handling  
    - Shopping cart with localStorage  
    - Checkout with stock validation and order saving  
    - Admin order management with stock rollback on deletion  
    - Role-based access control to protect routes  
    - Simple file-based data persistence using JSON  

---

## Repo Structure

    awe_electronice/
    ├── app.py # Main Flask application entry
    ├── models/
    │ └── customer.py # Customer model with password hashing
    ├── routes/
    │ ├── auth.py # Authentication routes
    │ ├── product.py # Product and checkout APIs
    │ └── order_api.py # Order management API routes
    ├── templates/ # HTML templates powered by Jinja2
    ├── static/
    │ ├── css/ # Stylesheets
    │ └── images/ # Uploaded product images
    ├── data/ # JSON files storing users, products, orders
    │ ├── customers.json
    │ ├── products.json
    │ └── orders.json
    ├── utils/
    │ └── json_handler.py # JSON read/write utilities
    └── README.md # This file


---

## Getting Started

### Prerequisites

- Python 3.8 or higher  
- Virtual environment tool (venv or virtualenv)  

### Installation and Running

1. Clone the repo:
    git clone https://github.com/aaradhyaaaronmaths555/awe_electronice.git
    cd awe_electronice

2. Create and activate a virtual environment:
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate

3. Install dependencies: pip install -r requirements.txt

4. Run the application: python app.py

5. Open your browser and go to: http://127.0.0.1:5000/products-page


Usage
            A)  Register a new user or log in as an existing user

            B) Admin login available at /admin with code: admin-admin

            C) Admin can upload products, manage stock, and view/delete orders

            D) Users can browse products, add to cart, and checkout securely

Notes
            A) Data persistence is file-based via JSON, located in the data/ folder

            B) Images uploaded are saved under static/images/

            C) The admin role is protected via session and a secret code; no JSON admin credentials needed

            D) The frontend uses Bootstrap and vanilla JavaScript with localStorage for the cart

