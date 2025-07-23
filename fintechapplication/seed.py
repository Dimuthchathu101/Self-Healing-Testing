from .app import app
from .db import db
from .models import User, Locator

def seed():
    db.drop_all()
    db.create_all()
    # Users
    user1 = User(username='alice', password='password', balance=1000)
    user2 = User(username='bob', password='password', balance=500)
    db.session.add_all([user1, user2])
    # Locators for login page
    db.session.add_all([
        Locator(page='login', element_name='username', selector_type='id', selector_value='login-username'),
        Locator(page='login', element_name='password', selector_type='id', selector_value='login-password'),
        Locator(page='login', element_name='login_btn', selector_type='id', selector_value='login-btn'),
    ])
    # Locators for dashboard
    db.session.add_all([
        Locator(page='dashboard', element_name='dashboard_title', selector_type='id', selector_value='dashboard-title'),
        Locator(page='dashboard', element_name='balance', selector_type='id', selector_value='dashboard-balance'),
        Locator(page='dashboard', element_name='transfer_btn', selector_type='id', selector_value='dashboard-transfer-btn'),
        Locator(page='dashboard', element_name='history_btn', selector_type='id', selector_value='dashboard-history-btn'),
    ])
    # Locator for notifications container (intentional: no locators for individual notifications)
    db.session.add(Locator(page='dashboard', element_name='notifications', selector_type='class', selector_value='notifications'))
    # Locators for transfer
    db.session.add_all([
        Locator(page='transfer', element_name='recipient', selector_type='id', selector_value='transfer-recipient'),
        Locator(page='transfer', element_name='amount', selector_type='id', selector_value='transfer-amount'),
        Locator(page='transfer', element_name='transfer_btn', selector_type='id', selector_value='transfer-btn'),
    ])
    # Locators for transactions (intentional issues: mismatched and missing locators)
    db.session.add_all([
        Locator(page='transactions', element_name='table', selector_type='id', selector_value='transactions-table'),
        Locator(page='transactions', element_name='row', selector_type='id', selector_value='transaction-row'),
        Locator(page='transactions', element_name='filter_btn', selector_type='id', selector_value='filter-button'),  # Does not match HTML id
        # No locator for search input or results table
    ])
    # Locators for profile (intentional issues: mismatched and duplicate IDs)
    db.session.add_all([
        Locator(page='profile', element_name='username', selector_type='id', selector_value='profile-username'),  # Does not match HTML id
        Locator(page='profile', element_name='email', selector_type='id', selector_value='profile-email-field'),
        Locator(page='profile', element_name='save_btn', selector_type='id', selector_value='profile-save-btn'),
    ])
    # Locators for billpay (intentional issues: mismatched and missing locators)
    db.session.add_all([
        Locator(page='billpay', element_name='vendor', selector_type='id', selector_value='bill-vendor'),  # Does not match HTML id
        # No locator for amount field
        # No locator for pay button (random id)
    ])
    # Locator for dark mode toggle (intentional mismatch)
    db.session.add(Locator(page='base', element_name='dark_toggle', selector_type='id', selector_value='darkmode-toggle'))  # HTML uses 'dark-toggle'
    db.session.commit()
    print('Database seeded!')

if __name__ == '__main__':
    with app.app_context():
    seed() 