from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pymysql

app = Flask(__name__)

# Configuration for MySQL connection
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'ofds'

# Function to establish a connection to the MySQL database
def connect_to_database():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

# Route for home page - Display list of restaurants
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/restaurants', methods=['GET', 'POST'])
def get_restaurants():
    connection = connect_to_database()
    cursor = connection.cursor()

    if request.method == 'POST':
        # Extract restaurant_id from form submission
        restaurant_id = request.form.get('restaurant_id')

        # Redirect to menu route with the selected restaurant_id
        return redirect(url_for('menu', restaurant_id=restaurant_id))
    
    try:
        # Query to fetch all restaurants
        query = "SELECT * FROM Restaurant"
        cursor.execute(query)
        restaurants = cursor.fetchall()
    except Exception as e:
        print("Error fetching restaurants:", e)
        restaurants = []  # Provide an empty list if there's an error

    # Close cursor and connection
    cursor.close()
    connection.close()

    return render_template('restaurants.html', restaurants=restaurants)


# Route for displaying the menu for a specific restaurant
@app.route('/menu/<int:restaurant_id>')
def menu(restaurant_id):
    # Connect to the database
    connection = connect_to_database()
    cursor = connection.cursor()

    # Query to fetch the restaurant name
    query = "SELECT RestaurantName FROM Restaurant WHERE RestaurantID = %s"
    cursor.execute(query, (restaurant_id,))
    restaurant_name = cursor.fetchone()[0]

    # Query to fetch menu items of the specific restaurant
    query = "SELECT * FROM Menu WHERE RestaurantID = %s"
    cursor.execute(query, (restaurant_id,))
    menu_items = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    connection.close()

    return render_template('menu.html', restaurant_name=restaurant_name, menu_items=menu_items)


# Route for creating a new customer
@app.route('/customers', methods=['GET', 'POST'])
def new_customer():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        payment_info = request.form['payment_info']

        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()

        # Query to insert new customer into the database
        query = "INSERT INTO Customer (CustomerName, CustomerEmail, CustomerAddress, CustomerPaymentInfo) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, address, payment_info))

        # Commit changes to the database
        connection.commit()

        # Close cursor and connection
        cursor.close()
        connection.close()

        return redirect(url_for('home'))

    return render_template('customers.html')

if __name__ == '__main__':
    app.run(debug=True)
