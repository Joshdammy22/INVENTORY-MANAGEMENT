from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(5), default="User")
    is_admin = db.Column(db.Boolean, default=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer, default=0)
    location = db.Column(db.String(100))
    barcode = db.Column(db.String(64), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', name='fk_product_category'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id', name='fk_product_supplier'))  # Named foreign key
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id', name='fk_product_purchase_order'))  # Named foreign key
    inventory = db.relationship('Inventory', backref='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.name}>'

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', name='fk_inventory_product'))
    quantity = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Inventory {self.product_id} - {self.quantity}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', name='fk_transaction_product'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_transaction_user'))
    transaction_type = db.Column(db.String(64))  # 'check-in', 'check-out', 'adjustment'
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.transaction_type} - {self.quantity}>'

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    contact_info = db.Column(db.String(120))
    products = db.relationship('Product', backref='supplier', lazy='dynamic')

    def __repr__(self):
        return f'<Supplier {self.name}>'

class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id', name='fk_purchase_order_supplier'))
    status = db.Column(db.String(64))  # 'pending', 'completed', 'cancelled'
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('Product', backref='purchase_order', lazy='dynamic')

    def __repr__(self):
        return f'<PurchaseOrder {self.id} - {self.status}>'
