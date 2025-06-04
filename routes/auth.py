from flask import Blueprint, request, redirect, render_template, session, flash
from models.customer import Customer
from utils.json_handler import load_json, save_json

import os
import uuid

auth = Blueprint('auth', __name__)

CUSTOMERS_FILE = 'data/customers.json'

# === REGISTER ===
@auth.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    customers = load_json(CUSTOMERS_FILE)

    if any(c['email'] == email for c in customers):
        flash("⚠️ Email already registered.", "danger")
        return redirect('/register-page')

    customer = Customer(
        id=str(uuid.uuid4()),
        name=name,
        email=email,
        password=password,
        hashed=False
    )
    customers.append(customer.to_dict())
    save_json(CUSTOMERS_FILE, customers)

    flash("✅ Registered successfully. You can now log in.", "success")
    return redirect('/login-page')


# === USER LOGIN ===
@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    customers = load_json(CUSTOMERS_FILE)

    for c in customers:
        customer = Customer(**c)
        if customer.email == email and customer.check_password(password):
            session['user'] = customer.email
            session['name'] = customer.name
            session['role'] = 'user'
            return redirect('/profile-page')

    flash("❌ Invalid credentials.", "danger")
    return redirect('/login-page')


# === ADMIN LOGIN (Simple Code Check) ===
@auth.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        code = request.form.get('code')
        if code == 'admin-admin':
            session['user'] = 'admin@awe.com'
            session['name'] = 'Admin'
            session['role'] = 'admin'
            return redirect('/admin-auth')
        else:
            return render_template('admin-verification.html', error="❌ Invalid admin code.")
    return render_template('admin-verification.html')


# === LOGOUT ===
@auth.route('/logout')
def logout():
    session.clear()
    return redirect('/login-page')
