from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Category


class LoginForm(FlaskForm):
    login = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('That username has been taken, please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('That email has been taken, please use a different email.')
class AdminForm(FlaskForm):
    # Example field, you can add more fields as required
    example_field = StringField('Example Field', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    location = StringField('Location')
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    supplier = SelectField('Supplier', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Product')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Add Category')

class InventoryForm(FlaskForm):
    product = SelectField('Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Update Inventory')

class TransactionForm(FlaskForm):
    product = SelectField('Product', coerce=int, validators=[DataRequired()])
    user = SelectField('User', coerce=int, validators=[DataRequired()])
    transaction_type = SelectField('Transaction Type', choices=[('check-in', 'Check-in'), ('check-out', 'Check-out'), ('adjustment', 'Adjustment')], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Log Transaction')

class SupplierForm(FlaskForm):
    name = StringField('Supplier Name', validators=[DataRequired()])
    contact_info = StringField('Contact Info', validators=[DataRequired()])
    submit = SubmitField('Add Supplier')

class PurchaseOrderForm(FlaskForm):
    supplier = SelectField('Supplier', coerce=int, validators=[DataRequired()])
    status = SelectField('Status', choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], validators=[DataRequired()])
    submit = SubmitField('Create Purchase Order')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')], validators=[DataRequired()])
    submit = SubmitField('Update')

class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete')

