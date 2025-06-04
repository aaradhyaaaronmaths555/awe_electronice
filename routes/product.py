from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

product = Blueprint('product', __name__)

UPLOAD_FOLDER = 'static/images'
DATA_FILE = 'data/products.json'
ORDERS_FILE = 'data/orders.json'

# Ensure data files exist
for file in [DATA_FILE, ORDERS_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)

@product.route('/api/products', methods=['GET'])
def get_products():
    with open(DATA_FILE) as f:
        return jsonify(json.load(f))

@product.route('/api/products', methods=['POST'])
def add_product():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    name = request.form.get('name')
    price = float(request.form.get('price', 0))
    stock = int(request.form.get('stock', 0))
    category = request.form.get('category')
    description = request.form.get('description', '')
    image_file = request.files.get('image')

    if image_file:
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        image_file.save(image_path)
        image_url = f'/static/images/{filename}'
    else:
        image_url = '/static/images/default.jpg'

    with open(DATA_FILE, 'r') as f:
        products = json.load(f)

    new_id = max([p['id'] for p in products], default=0) + 1
    new_product = {
        "id": new_id,
        "name": name,
        "price": price,
        "stock": stock,
        "category": category,
        "description": description,
        "image": image_url
    }

    products.append(new_product)

    with open(DATA_FILE, 'w') as f:
        json.dump(products, f, indent=2)

    return jsonify({"message": "Product added successfully", "product": new_product}), 201

@product.route('/api/checkout', methods=['POST'])
def checkout_products():
    if 'user' not in session:
        return jsonify({"error": "Not logged in"}), 403

    if session.get('role') == 'admin':
        return jsonify({"error": "Admins cannot purchase products. Please log in as a user."}), 403

    data = request.get_json()
    cart = data.get('cart', [])
    shipping_name = data.get('name')
    shipping_address = data.get('address')

    with open(DATA_FILE, 'r') as f:
        products = json.load(f)

    # Validate stock availability
    for item in cart:
        product_item = next((p for p in products if p['id'] == item['id']), None)
        if not product_item:
            return jsonify({"error": f"Product ID {item['id']} not found."}), 400
        if product_item['stock'] == 0:
            return jsonify({"error": f"{product_item['name']} is out of stock."}), 400
        if product_item['stock'] < item['quantity']:
            return jsonify({"error": f"Not enough stock for {product_item['name']}."}), 400

    # Deduct stock
    for item in cart:
        for p in products:
            if p['id'] == item['id']:
                p['stock'] -= item['quantity']

    with open(DATA_FILE, 'w') as f:
        json.dump(products, f, indent=2)

    # Record order
    with open(ORDERS_FILE, 'r') as f:
        orders = json.load(f)

    total_price = sum(
        item['quantity'] * next((p['price'] for p in products if p['id'] == item['id']), 0)
        for item in cart
    )

    new_order = {
        "email": session['user'],
        "name": session.get('name', 'Unknown'),
        "cart": cart,
        "total": total_price,
        "shipping_name": shipping_name,
        "shipping_address": shipping_address,
        "timestamp": datetime.now().isoformat()
    }

    orders.append(new_order)

    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=2)

    return jsonify({"message": "Order placed successfully", "products": products})

@product.route('/api/products/update/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    with open(DATA_FILE, 'r') as f:
        products = json.load(f)

    for p in products:
        if p['id'] == id:
            p['stock'] = data.get('stock', p['stock'])

    with open(DATA_FILE, 'w') as f:
        json.dump(products, f, indent=2)

    return jsonify({"message": "Product updated successfully"})

@product.route('/api/products/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    with open(DATA_FILE, 'r') as f:
        products = json.load(f)

    products = [p for p in products if p['id'] != id]

    with open(DATA_FILE, 'w') as f:
        json.dump(products, f, indent=2)

    return jsonify({"message": "Product deleted successfully"})
