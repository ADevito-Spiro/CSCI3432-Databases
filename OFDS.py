from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pymysql

app = Flask(__name__)

# Configuration for MySQL connection
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'OFDS'

# Function to establish a connection to the MySQL database
def connect_to_database():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

# Route for home page - Display list of restaurants
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        connection = connect_to_database()
        cursor = connection.cursor()

        query = "SELECT CustomerID FROM Customer WHERE CustomerEmail = %s"
        cursor.execute(query, (email,))
        customer_id = cursor.fetchone()

        if customer_id is not None:
            customer_id = customer_id[0]
            connection.close()
            cursor.close()
            return redirect(url_for('customer_home', customer_id=customer_id))
        else:
            # If the email does not exist in the database, redirect to the new_customer route
            return redirect(url_for('new_customer', email=email))
    
    # For GET requests, render the login template
    return render_template('login.html')

@app.route('/restaurants', methods=['GET', 'POST'])
def get_restaurants():
    if request.method == 'POST':
        restaurant_id = request.values.get('restaurant_id')
        print(restaurant_id)
        return redirect(url_for('menu', restaurant_id=restaurant_id))

    connection = connect_to_database()
    cursor = connection.cursor()

    query = "Select * From Restaurant Where Approved = TRUE"
    cursor.execute(query)
    restaurants = cursor.fetchall()

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

        query = "Select COUNT(*) From Customer WHERE CustomerEmail = %s"
        cursor.execute(query, (email,))
        existing = cursor.fetchone()[0]

        if existing > 0:
            error_message = "An account already exists for this email"
            return render_template('customers.html', error_message=error_message)
        else:
            # Query to insert new customer into the database
            query = "INSERT INTO Customer (CustomerName, CustomerEmail, CustomerAddress, CustomerPaymentType) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, address, payment_info))

            # Commit changes to the database
            connection.commit()

            customer_id=cursor.lastrowid

            # Close cursor and connection
            cursor.close()
            connection.close()
            return redirect(url_for('customer_home',customer_id=customer_id))
    return render_template('customers.html')

@app.route('/customer_home/<int:customer_id>', methods=['GET', 'POST'])
def customer_home(customer_id):
    if request.method == 'POST':
        try:
            # Connect to the database
            connection = connect_to_database()
            cursor = connection.cursor()

            # Fetch recent orders for the selected customer
            query = "SELECT * FROM Orders WHERE CustomerID = %s"
            cursor.execute(query, (customer_id,))
            recent_orders = cursor.fetchall()

            # Fetch customer name for the selected customer
            query = "SELECT CustomerName FROM Customer WHERE CustomerID = %s"
            cursor.execute(query, (customer_id,))
            customer_name = cursor.fetchone()[0]

            # Close cursor and connection
            cursor.close()
            connection.close()

            return render_template('customer_home.html', recent_orders=recent_orders, customer_name=customer_name)
        except Exception as e:
            # Handle errors
            print("Error fetching recent orders:", e)
            return "Error fetching recent orders", 500  # Return an error message with status code 500
    else:
        # Display the page initially with no specific customer selected
        return render_template('customer_home.html', recent_orders=[], customer_id=customer_id)

# Route to display all customers
@app.route('/edit_customer', methods=['GET'])
def edit_customers():
    connection = connect_to_database()
    cursor = connection.cursor()

    # Fetch all customers from the database
    query = "SELECT * FROM Customer"
    cursor.execute(query)
    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('edit_customer.html', customers=customers)

@app.route('/edit_single_customer', methods=['POST'])
def edit_single_customer():
    if request.method == 'POST':
        # Retrieve form data
        customer_id = request.form['customer_id']
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        payment_info = request.form['payment_info']

        try:
            # Connect to the database
            connection = connect_to_database()
            cursor = connection.cursor()

            # Update customer data in the database
            query = "UPDATE Customer SET CustomerName = %s, CustomerEmail = %s, CustomerAddress = %s, CustomerPaymentType = %s WHERE CustomerID = %s"
            cursor.execute(query, (name, email, address, payment_info, customer_id))
            connection.commit()

            # Close cursor and connection
            cursor.close()
            connection.close()

            return redirect(url_for('edit_customers'))  # Redirect to the edit_customer page after successful update
        except Exception as e:
            # Handle errors
            print("Error updating customer data:", e)
            return "Error updating customer data", 500  # Return an error message with status code 500
    else:
        return redirect(url_for('edit_customers'))  # Redirect to the edit_customer page if not a POST request

# Route to handle deleting a customer
@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    if request.method == 'POST':
        customer_id = request.form['customer_id']

        connection = connect_to_database()
        cursor = connection.cursor()

        # Delete the customer from the database
        query = "DELETE FROM Customer WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('edit_customers'))

@app.route('/restaurants/update', methods=['GET', 'POST'])
def update_restaurant():
    if request.method == 'POST':
        restaurant_id = request.form['restaurant_id']
        menu_item = request.form['menu_item']
        item_desc = request.form['item_desc']
        item_price = request.form['item_price']
        location = request.form['location']

        connection = connect_to_database()
        cursor = connection.cursor()

        query = "INSERT INTO Menu (RestaurantID, MenuItem, MenuItemDesc, MenuItemPrice) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (restaurant_id, menu_item, item_desc, item_price))

        query = "UPDATE Restaurant SET RestaurantLocation = %s WHERE RestaurantID = %s"
        cursor.execute(query, (location, restaurant_id))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('home'))

    return render_template('update_restaurant.html')

@app.route('/admin/restaurants/action', methods=['GET', 'POST'])
def handle_restaurant_action():
    connection = connect_to_database()
    cursor = connection.cursor()

    if request.method == 'POST':
        restaurant_id = request.form['restaurant_id']
        action = request.form['action']

        if action == 'approve':
            query = "UPDATE Restaurant SET Approved = TRUE WHERE RestaurantID = %s"
        elif action == 'unapprove':
            query = "UPDATE Restaurant SET Approved = FALSE WHERE RestaurantID = %s"
        else:
            # Handle invalid action
            return "Invalid action", 400

        cursor.execute(query, (restaurant_id,))
        connection.commit()

    # Query unapproved restaurants
    query_unapproved = "SELECT * FROM Restaurant WHERE Approved = FALSE"
    cursor.execute(query_unapproved)
    unapproved_restaurants = cursor.fetchall()

    # Query approved restaurants
    query_all = "SELECT * FROM Restaurant WHERE Approved = TRUE"
    cursor.execute(query_all)
    all_restaurants = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('admin_restaurants.html', unapproved_restaurants=unapproved_restaurants, all_restaurants=all_restaurants)

if __name__ == '__main__':
    app.run(debug=True)
