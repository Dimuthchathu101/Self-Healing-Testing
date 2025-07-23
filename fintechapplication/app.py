from flask import Flask, render_template, redirect, url_for, request, session, g
from .db import db
import os
from .models import User, Transaction, Locator
from werkzeug.security import check_password_hash
from flask import flash
from datetime import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'fintech.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from .models import User, Transaction, Locator

# Utility to get locators for a page

def get_locators(page):
    locators = Locator.query.filter_by(page=page).all()
    locator_dict = {l.element_name: {'type': l.selector_type, 'value': l.selector_value} for l in locators}
    # Fallback/defaults for login page
    if page == 'login':
        defaults = {
            'username': {'type': 'id', 'value': 'login-username'},
            'password': {'type': 'id', 'value': 'login-password'},
            'login_btn': {'type': 'id', 'value': 'login-btn'},
        }
        for k, v in defaults.items():
            if k not in locator_dict:
                print(f"[WARNING] Missing locator for '{k}' on page 'login', using default.")
                locator_dict[k] = v
    return locator_dict

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    locators = get_locators('login')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', locators=locators, error=error)

# Dummy notifications data
NOTIFICATIONS = [
    {'msg': 'Your account was credited with $100.', 'type': 'success'},
    {'msg': 'Scheduled maintenance on Friday.', 'type': 'info'},
    {'msg': 'Unusual login detected.', 'type': 'warning'},
]

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    locators = get_locators('dashboard')
    # Pass notifications to template
    return render_template('dashboard.html', username=user.username, balance=user.balance, locators=locators, notifications=NOTIFICATIONS)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    error = None
    success = None
    locators = get_locators('transfer')
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        recipient_username = request.form['recipient']
        amount = float(request.form['amount'])
        recipient = User.query.filter_by(username=recipient_username).first()
        if not recipient:
            error = 'Recipient not found.'
        elif amount <= 0 or amount > user.balance:
            error = 'Invalid amount.'
        else:
            user.balance -= amount
            recipient.balance += amount
            db.session.add(Transaction(user_id=user.id, amount=-amount, type='transfer', timestamp=datetime.now()))
            db.session.add(Transaction(user_id=recipient.id, amount=amount, type='transfer', timestamp=datetime.now()))
            db.session.commit()
            success = f'Transferred ${amount} to {recipient_username}.'
    return render_template('transfer.html', locators=locators, error=error, success=success)

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    txns = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.timestamp.desc()).all()
    locators = get_locators('transactions')
    filtered = False
    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()
        if search_query:
            txns = [t for t in txns if search_query.lower() in t.type.lower() or search_query in str(t.amount)]
            filtered = True
    return render_template('transactions.html', transactions=txns, locators=locators, filtered=filtered, search_query=search_query)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    locators = get_locators('profile')
    message = None
    if request.method == 'POST':
        # Intentional issue: mismatch field name in HTML vs. here
        user.username = request.form.get('profile_username', user.username)
        db.session.commit()
        message = 'Profile updated!'
    return render_template('profile.html', user=user, locators=locators, message=message)

@app.route('/billpay', methods=['GET', 'POST'])
def billpay():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    locators = get_locators('billpay')
    message = None
    # Intentional issue: randomize the pay button id
    random_id = f"pay-btn-{random.randint(1000,9999)}"
    if request.method == 'POST':
        # Intentional issue: mismatch field name in HTML vs. here
        vendor = request.form.get('bill_vendor')
        amount = request.form.get('bill_amount')
        if vendor and amount:
            message = f'Paid ${amount} to {vendor}!'
    return render_template('billpay.html', locators=locators, message=message, random_id=random_id)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Placeholder for models and routes

def create_tables():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True) 