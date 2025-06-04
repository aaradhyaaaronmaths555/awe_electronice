from flask import Blueprint, request, jsonify
import json
import os

order_api = Blueprint('order_api', __name__)

ORDERS_FILE = 'data/orders.json'
PRODUCTS_FILE = 'data/products.json'

def load_json(path):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump([], f)
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

@order_api.route('/api/orders/delete', methods=['POST'])
def delete_order():
    data = request.get_json()
    timestamp_to_delete = data.get('timestamp')

    if not timestamp_to_delete:
        return jsonify({'error': 'Timestamp is required'}), 400

    orders = load_json(ORDERS_FILE)
    order_to_delete = None
    for order in orders:
        if order.get('timestamp') == timestamp_to_delete:
            order_to_delete = order
            break

    if not order_to_delete:
        return jsonify({'error': 'Order not found'}), 404

    # Load products and restock items
    products = load_json(PRODUCTS_FILE)
    for item in order_to_delete.get('cart', []):
        product_id = item['id']
        qty = item['quantity']
        for p in products:
            if p['id'] == product_id:
                p['stock'] += qty
                break

    save_json(PRODUCTS_FILE, products)

    # Remove the order and save orders.json
    orders = [o for o in orders if o.get('timestamp') != timestamp_to_delete]
    save_json(ORDERS_FILE, orders)

    return jsonify({'message': 'Order deleted and stock updated successfully'}), 200
