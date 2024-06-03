from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from urllib.parse import urlsplit  
from flask_login import current_user, login_user, logout_user, login_required
from functools import wraps

def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                flash('You do not have permission to access this page.')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/admin')
@login_required
@role_required('admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', title='Admin', users=users)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')



@app.route('/')
@app.route('/home')
#@login_required
def home():
    return render_template('home.html', title='Home')

@app.route('/inventory')
@login_required
def inventory():
    products = Product.query.all()
    return render_template('inventory.html', title='Inventory', products=products)


@app.route('/categories')
@login_required
def categories():
    categories = Category.query.all()
    return render_template('categories.html', title='Categories', categories=categories)

@app.route('/transactions')
@login_required
def transactions():
    transactions = Transaction.query.all()
    return render_template('transactions.html', title='Transactions', transactions=transactions)

# @app.route('/product/add', methods=['GET', 'POST'])
# @login_required
# def add_product():
#     if request.method == 'POST':
#         name = request.form['name']
#         description = request.form['description']
#         quantity = int(request.form['quantity'])
#         category_id = int(request.form['category'])
#         product = Product(name=name, description=description, quantity=quantity, category_id=category_id, user_id=current_user.id)
#         db.session.add(product)
#         db.session.commit()
#         flash('Product added successfully!')
#         return redirect(url_for('inventory'))
#     categories = Category.query.all()
#     return render_template('add_product.html', title='Add Product', categories=categories)


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    form.supplier.choices = [(s.id, s.name) for s in Supplier.query.all()]
    if form.validate_on_submit():
        product = Product(
            name=form.name.data, 
            description=form.description.data, 
            price=form.price.data, 
            quantity=form.quantity.data, 
            location=form.location.data, 
            category_id=form.category.data,
            supplier_id=form.supplier.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('home'))
    return render_template('add_product.html', title='Add Product', form=form)

@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!')
        return redirect(url_for('home'))
    return render_template('add_category.html', title='Add Category', form=form)



@app.route('/update_inventory', methods=['GET', 'POST'])
@login_required
def update_inventory():
    form = InventoryForm()
    form.product.choices = [(p.id, p.name) for p in Product.query.all()]
    if form.validate_on_submit():
        inventory = Inventory(product_id=form.product.data, quantity=form.quantity.data)
        db.session.add(inventory)
        db.session.commit()
        flash('Inventory updated successfully!')
        return redirect(url_for('home'))
    return render_template('update_inventory.html', title='Update Inventory', form=form)


@app.route('/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.quantity = int(request.form['quantity'])
        product.category_id = int(request.form['category'])
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('inventory'))
    categories = Category.query.all()
    return render_template('edit_product.html', title='Edit Product', product=product, categories=categories)

@app.route('/product/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('inventory'))


@app.route('/suppliers')
@login_required
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', title='Suppliers', suppliers=suppliers)

@app.route('/purchase_orders')
@login_required
def purchase_orders():
    purchase_orders = PurchaseOrder.query.all()
    return render_template('purchase_orders.html', title='Purchase Orders', purchase_orders=purchase_orders)



@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash('User updated successfully!')
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.role.data = user.role
    return render_template('edit_user.html', title='Edit User', form=form)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!')
    return redirect(url_for('admin'))
