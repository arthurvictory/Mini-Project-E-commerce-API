from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from datetime import datetime
from datetime import timedelta
from marshmallow import fields
from marshmallow import ValidationError

# connect to database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Mp261Vk823!@localhost/e_commerce_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app,db)

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
    customer_id = fields.Integer(required=True)

    class Meta:
        fields = ('username','password','customer_id')

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
    order_date = fields.Date(required=True)
    user_id = fields.Integer(required=True)
    total_price = fields.Float(required=True)
    customer_id = fields.Integer(required=True)
    product_ids = fields.List(fields.Integer, required=True) 

    class Meta:
        fields = ("date", "user_id", "total_price", "customer_id", "product_ids")
    
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# Create tables and relationships in databases
class Customer(db.Model):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(320))
    phone = db.Column(db.String(15))

class Order(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'), nullable=False)
    customer = db.relationship('Customer', backref='orders')
    status = db.Column(db.String(50), nullable=False, default="Processing") 

    products = db.relationship('Product', secondary='Order_Product', lazy='subquery', backref=db.backref('orders', lazy=True))

class CustomerAccount(db.Model):
    __tablename__ = 'Customer_Accounts'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'), nullable=False)
    customer = db.relationship('Customer', backref = 'customer_account', uselist = False)

order_product = db.Table('Order_Product',
    db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('Products.id'), primary_key=True)
)

class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Integer, nullable=False)

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
    
    new_customer = Customer(name = customer_data['name'], email = customer_data['email'], phone = customer_data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "New customer added to database!"}), 201

# update a customer to the database
@app.route("/customers/<int:id>", methods=["PUT"])
def update_customers(id):
    customer = Customer.query.get_or_404(id)
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.phone = customer_data['phone']
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
    
    new_account = CustomerAccount(username = account_data['username'], password = account_data['password'], customer_id = account_data['customer_id'])
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
    
    account.username = account_data['username']
    account.password = account_data['password']
    account.customer_id = account_data['customer_id']
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
    return products_schema.jsonify(products)

# create a product in the database
@app.route('/products', methods = ['POST'])
def add_products():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_product = Product(name = product_data['name'], price = product_data['price'], quantity = product_data['quantity'])
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
    product.price = product_data['price']
    product.quantity = product_data['quantity']
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
        new_order = Order(
            customer_id=order_data['customer_id'],
            products=[Product.query.get(pid) for pid in order_data['product_ids']]
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "Order placed successfully!", "order_id": new_order.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/orders/<int:id>', methods=['GET'])
def retrieve_orders(id):
    order = Order.query.get_or_404(id)
    return jsonify({
        "order_id": order.id,
        "customer_id": order.customer_id,
        "order_date": order.order_date,
        "status": order.status,
        "products": [{"id": p.id, "name": p.name, "price": p.price} for p in order.products]
    })

@app.route('/orders/<int:id>/track', methods=['GET'])
def track_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({
        "order_id": order.id,
        "status": order.status,
        "order_date": order.order_date,
        "expected_delivery": (order.order_date + timedelta(days=5)).strftime("%Y-%m-%d")
    })

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug = True)