from .app import app
from .db import db
from .models import User
 
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"Username: {user.username}, Password: {user.password}, Balance: {user.balance}") 