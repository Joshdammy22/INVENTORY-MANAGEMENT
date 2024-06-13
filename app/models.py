from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from flask_sqlalchemy import SQLAlchemy


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(5), default="Staff")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(255))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    location = db.Column(db.String(128))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))

    def __repr__(self):
        return f'<Product {self.name}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    location = db.Column(db.String(128))
    address = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone_number = db.Column(db.String(15))
    product = db.Column(db.String(64))

    def __repr__(self):
        return f'<Supplier {self.name}>'

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Inventory {self.product_id} - {self.quantity}>'

class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<PurchaseOrder {self.product_id} - {self.quantity}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(20), default='Pending')
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Order {self.id}>'


