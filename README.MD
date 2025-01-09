# E-Commerce API

This is a Flask-based REST API designed to manage an e-commerce system. It allows users to manage products, orders, customer accounts, and user details.

## Features
This uses SQLAlchemy to handle all CRUD operations of the following:
User Management, Customer Account Management, Product Management and Order Management

## Installation
Prerequisites
Python 3.x
MySQL Database
Install the required Python packages:
bash
Copy code
pip install Flask Flask-SQLAlchemy Flask-Marshmallow marshmallow mysql-connector
Database Setup
Create MySQL Database: Create a MySQL database named e_test_db (or modify the SQLALCHEMY_DATABASE_URI to point to your existing database).
Create Tables: The tables will be automatically created when the app is run. Ensure your MySQL server is running.

## Configuration
Database Connection: Modify the connection string in the app to reflect your MySQL credentials and database name:
python
Copy code
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:(enter password here)@localhost/e_test_db'

## Running the App
To run the app, simply execute the following command:
Copy code
Run python app.py in command terminal
This will start the Flask development server on http://127.0.0.1:5000/.


This is a simple and flexible API to handle user, product, account, and order management for an e-commerce platform. You can extend this application further with more advanced features like payment processing, inventory management, etc.