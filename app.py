from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow import ValidationError

# connect to database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Mp261Vk823!@localhost/e_commerce_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define schemas for databases
class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ('name','email','phone','id')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

class AccountSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        fields = ('username','password','user_id')

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)

class ProductSchema(ma.Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True)
    quantity = fields.Integer(required=True)

    class Meta:
        fields = ('name','price','quantity','id')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class OrderSchema(ma.Schema):
    date = fields.String(required=True)
    user_id = fields.Integer(required=True)
    total_price = fields.Float(required=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# Create tables and relationships in databases
class Customer(db.Model):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(320))
    phone = db.Column(db.String(15))
    orders = db.relationship('Order', backref = 'customer')

class Order(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))

class CustomerAccount(db.Model):
    __tablename__ = 'Customer_Accounts'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))
    customer = db.relationship('Customer', backref = 'customer_account', uselist = False)

order_product = db.Table('Order_Product',
        db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'), primary_key = True),
        db.Column('product_id', db.Integer, db.ForeignKey('Products.id', primary_key = True))
)

class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    orders = db.relationship('Order', secondary = order_product, backref = db.backref('products'))

@app.route('/')
def home():
    return "Welcome to the E-Commerce API Database!"

# Creating CRUD operations for Customers

# list all customers in the database
@app.route('/customers', methods = ['GET'])
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers)

# add a customer to the database
@app.route('/customers', methods = ['POST'])
def add_customers():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_customer = Customer(id = customer_data['id'], name = customer_data['name'], email = customer_data['email'], phone = customer_data['phone'], orders = customer_data['orders'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "New customer and order added to database!"}), 201

# update a customer to the database
@app.route("/customers/<int:id>", methods=["PUT"])
def update_customers(id):
    customer = Customer.query.get_or_404(id)
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer.name = customer_data['name']
    customer.age = customer_data['age']
    db.session.commit()
    return jsonify({"message": "Customer details have updated successfully"}), 200

# Delete the customer to the database
@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customers(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer has been deleted successfully"}), 200

# Creating CRUD operations for CustomerAccounts

# list all accounts in Customer Accounts
@app.route('/customer_accounts', methods = ['GET'])
def get_accounts():
    accounts = CustomerAccount.query.all()
    return accounts_schema.jsonify(accounts)

# Add customer to database
@app.route('/customer_accounts', methods = ['POST'])
def add_accounts():
    try:
        account_data = account_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_account = Customer(username = account_data['username'], password = account_data['password'], customer_id = account_data['customer_id'])
    db.session.add(new_account)
    db.session.commit()
    return jsonify({"message": "New customer account has been added to database!"}), 201

# Update endpoint to customer accounts
@app.route("/customer_accounts/<int:id>", methods=["PUT"])
def update_accounts(id):
    account = CustomerAccount.query.get_or_404(id)
    try:
        account_data = account_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    account.name = account_data['name']
    account.age = account_data['age']
    db.session.commit()
    return jsonify({"message": "Customer Account has updated successfully"}), 200

# Delete customer from database
@app.route("/customer_accounts/<int:id>", methods=["DELETE"])
def delete_accounts(id):
    account = CustomerAccount.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Customer account has been deleted successfully"}), 200

#Create CRUD operations for products

# list all products in the database
@app.route('/products', methods = ['GET'])
def get_products():
    products = Product.query.all()
    return accounts_schema.jsonify(products)

# create a product in the databas
@app.route('/products', methods = ['POST'])
def add_products():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_product = Customer(name = product_data['name'], price = product_data['price'], quantity = product_data['quantity'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "New product has been added to database!"}), 201

# Get a certain product by id
@app.route('/products/<int:id>', methods = ['GET'])
def read_products(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)

# Update a product already in the database
@app.route("/products/<int:id>", methods=["PUT"])
def update_products(id):
    product = Product.query.get_or_404(id)
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    product.name = product_data['name']
    product.age = product_data['age']
    db.session.commit()
    return jsonify({"message": "Product details have updated successfully"}), 200

# Delete a product in the database
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_products(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product has been deleted successfully"}), 200

# Create CRUD operations for Orders

# Endpoint to create new order
@app.route('/orders', methods = ['POST'])
def create_orders():
    try:
        order_data = order_schema.load(request.json)
        product = Product.query.all()
        price = 0
        for item in product:
            product = Product.query.get(item['id'])
            price += product.price * item['quantity']
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_order = Customer(date = order_data['date'], customer_id = order_data['customer_id'], price = price)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "New order added to database!"}), 201

@app.route('/orders/<int:id>', methods=['GET'])
def retrieve_orders(id):
    order = Order.query.get_or_404(id)
    return order_schema.jsonify(order)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug = True)