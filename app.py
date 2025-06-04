from flask import Flask, render_template, session, redirect, flash
from flask_cors import CORS

from routes.auth import auth
from routes.product import product
from routes.order_api import order_api  # Make sure this file exists!

app = Flask(__name__)
app.secret_key = 'awe-secret'
CORS(app, supports_credentials=True)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(product)
app.register_blueprint(order_api)

# Routes
@app.route('/')
def home():
    return {'message': 'AWE Electronics Backend is Live'}

@app.route('/register-page')
def register_page():
    return render_template('register.html')

@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/profile-page')
def profile_page():
    return render_template('profile.html')

@app.route('/products-page')
def products_page():
    return render_template('products.html')

@app.route('/upload-page')
def upload_page():
    if session.get('role') != 'admin':
        flash("You must be logged in as admin to access this page.", "warning")
        return redirect('/login-page')
    return render_template('upload.html')

@app.route('/cart-page')
def cart_page():
    if session.get('role') == 'admin':
        flash("Admins cannot buy products. Please log in as a user to purchase.", "warning")
        return redirect('/login-page')
    return render_template('cart.html')

@app.route('/admin-auth')
def admin_auth():
    return render_template('admin-auth.html')

@app.route('/admin-products')
def admin_products():
    if session.get('role') != 'admin':
        flash("You must be logged in as admin to access this page.", "warning")
        return redirect('/login-page')
    return render_template('admin-products.html')

@app.route('/view-orders')
def view_orders():
    if session.get('role') != 'admin':
        flash("You must be logged in as admin to access this page.", "warning")
        return redirect('/login-page')

    import json
    with open('data/orders.json', 'r') as f:
        orders = json.load(f)
    return render_template('view-orders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
