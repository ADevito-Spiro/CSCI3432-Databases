from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'OFDS'

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

        # Check if the username and password are correct
        if email == 'admin@admin.com':
            session['logged_in'] = True  # Set session variable to indicate user is logged in
            return redirect(url_for('handle_restaurant_action'))

        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()

        # Query to check if the email exists in the Customer table
        query = "SELECT CustomerID FROM Customer WHERE CustomerEmail = %s"
        cursor.execute(query, (email,))
        customer_id = cursor.fetchone()

        if customer_id is not None:
            customer_id = customer_id[0]
            session['customer_id'] = customer_id[0]
            connection.close()
            cursor.close()
            session['logged_in'] = True  # Set session variable to indicate user is logged in
            return redirect(url_for('customer_home', customer_id=customer_id))
        else:
            connection.close()
            cursor.close()
            # If the email does not exist in the database, redirect to the new_customer route
            return redirect(url_for('new_customer', email=email))

    # For GET requests or if login was unsuccessful, render the login template
    return render_template('login.html')

@app.route('/restaurants', methods=['GET', 'POST'])
def get_restaurants():
    if request.method == 'POST':
        restaurant_id = request.form.get('restaurant_id')
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

@app.route('/menu/<int:restaurant_id>', methods=['GET', 'POST'])
def menu(restaurant_id):
    if 'logged_in' not in session or not session['logged_in']:
        flash("Please log in to place an order.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get the selected menu item from the form
        selected_item = request.form.get('selected_item')

        # Validate if the selected item is not empty
        if not selected_item:
            flash("Please select a menu item.", "error")
            return redirect(url_for('menu', restaurant_id=restaurant_id))

        # Here, you can process the order submission, such as adding the item to the cart
        # For demonstration purposes, we'll just append the item to the cart in the session
        if 'cart' not in session:
            session['cart'] = []

        session['cart'].append(selected_item)

        flash("Order placed successfully!", "success")
        return redirect(url_for('view_cart'))

    # If it's a GET request, retrieve the restaurant's menu items and render the menu page
    # Connect to the database
    connection = connect_to_database()
    cursor = connection.cursor()

    # Query to fetch the restaurant name
    query = "SELECT RestaurantName FROM Restaurant WHERE RestaurantID = %s"
    cursor.execute(query, (restaurant_id,))
    restaurant_name = cursor.fetchone()[0]

    query = "SELECT MenuItem, MenuItemDesc, MenuItemPrice FROM Menu WHERE RestaurantID = %s"
    cursor.execute(query, (restaurant_id,))
    menu_items = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    connection.close()

    # Fetch user information
    if 'customer_id' in session:
        connection = connect_to_database()
        cursor = connection.cursor()

        customer_id = session['customer_id']
        
        # You can retrieve additional details of items from the database if needed
        query = "SELECT CustomerName, CustomerEmail, CustomerAddress FROM Customer WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        name, email, address = cursor.fetchone()

        cursor.close()
        connection.close()

        return render_template('cart.html', restaurant_name=restaurant_name, menu_items=menu_items, restaurant_id=restaurant_id,
                               customer_id=customer_id, name=name, email=email, address=address)
    else:
        return render_template('menu.html', restaurant_name=restaurant_name, menu_items=menu_items, restaurant_id=restaurant_id)

@app.route('/view_cart')
def view_cart():
    # Check if 'cart' exists in session, if not, initialize it as an empty list
    if 'cart' not in session:
        session['cart'] = []
    
    # Fetch the cart items from the session
    cart_items = session['cart']

    # Fetch user information
    if 'customer_id' in session:
        connection = connect_to_database()
        cursor = connection.cursor()

        customer_id = session['customer_id']
        
        # You can retrieve additional details of items from the database if needed
        query = "SELECT CustomerName, CustomerEmail, CustomerAddress FROM Customer WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        name, email, address = cursor.fetchone()

        cursor.close()
        connection.close()

        return render_template('cart.html', customer_id=customer_id,cart_items=cart_items, name=name, email=email, address=address)
    else:
        return render_template('cart.html', cart_items=cart_items)


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
    customer_id=customer_id
    if request.method == 'POST':
        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            # Fetch customer name for the selected customer
            query = "SELECT CustomerName FROM Customer WHERE CustomerID = %s"
            cursor.execute(query, (customer_id,))
            customer_name = cursor.fetchone()[0]

            # Close cursor and connection
            cursor.close()
            connection.close()

            # Display the page initially with no specific customer selected
            return render_template('customer_home.html', customer_name=customer_name)

        except Exception as e:
            # Handle errors
            print("Error fetching recent orders:", e)
            return "Error fetching recent orders", 500  # Return an error message with status code 500
    else:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Fetch customer name for the selected customer
        query = "SELECT CustomerName FROM Customer WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        customer_name = cursor.fetchone()[0]

        # Fetch recent orders for the selected customer
        query = "SELECT OrdersID FROM Orders WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        order_ids = cursor.fetchall()

        drivers = []
        order_dates = []
        total_prices = []

        # Fetch additional details for each order
        for order_id in order_ids:
            # Fetch driver details
            driver_query = "SELECT DriverName, CurrentDriverLocation FROM Driver WHERE OrdersID = %s"
            cursor.execute(driver_query, (order_id,))
            driver_details = cursor.fetchone()
            drivers.append(driver_details)

            # Fetch time of order
            time_query = "SELECT TimeOfOrder FROM DateOrder WHERE OrdersID = %s"
            cursor.execute(time_query, (order_id,))
            time_of_order = cursor.fetchone()[0]
            order_dates.append(time_of_order)

            # Fetch total cart
            total_query = "SELECT TotalCart FROM Price WHERE OrdersID = %s"
            cursor.execute(total_query, (order_id,))
            total_cart = cursor.fetchone()[0]
            total_prices.append(total_cart)

        # Close cursor and connection
        cursor.close()
        connection.close()

        # Display the page initially with no specific customer selected
        return render_template('customer_home.html', customer_id=customer_id, customer_name=customer_name, drivers=drivers, order_dates=order_dates, total_prices=total_prices, order_ids=order_ids)

@app.route('/self_edit/<int:customer_id>', methods=['POST'])
def self_edit(customer_id):
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    payment_info = request.form['payment_type']

    connection = connect_to_database()
    cursor = connection.cursor()

    query = "UPDATE Customer SET CustomerName = %s, CustomerEmail = %s, CustomerAddress = %s, CustomerPaymentType = %s WHERE CustomerID = %s"
    cursor.execute(query, (name, email, address, payment_info, customer_id))
    
    connection.commit()

    # Fetch updated customer data
    cursor.execute("SELECT * FROM Customer WHERE CustomerID = %s", (customer_id,))
    customer = cursor.fetchone()

    cursor.close()
    connection.close()
    
    # Return the updated customer data or redirect to the customer home page
    if customer:
        return redirect(url_for('customer_home', customer_id=customer_id))
    else:
        return "Customer not found", 404

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
    connection = connect_to_database()
    cursor = connection.cursor()

    # Fetch all customers from the database
    query = "SELECT * FROM Restaurant"
    cursor.execute(query)
    restaurants = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('update_restaurant.html', restaurants=restaurants)

@app.route('/update_restaurant', methods=['POST'])
def update_single_restaurant():
    if request.method == 'POST':
        # Retrieve form data
        restaurant_id = request.form['restaurant_id']
        description = request.form['description']
        location = request.form['location']

        try:
            # Connect to the database
            connection = connect_to_database()
            cursor = connection.cursor()

            # Update restaurant data in the database
            query = "UPDATE Restaurant SET RestaurantDesc = %s, RestaurantLocation = %s WHERE RestaurantID = %s"
            cursor.execute(query, (description, location, restaurant_id))
            connection.commit()

            # Close cursor and connection
            cursor.close()
            connection.close()

            return redirect(url_for('edit_restaurants'))  # Redirect to the edit_restaurants page after successful update
        except Exception as e:
            # Handle errors
            print("Error updating restaurant data:", e)
            return "Error updating restaurant data", 500  # Return an error message with status code 500
    else:
        return redirect(url_for('edit_restaurants'))  # Redirect to the edit_restaurants page if not a POST request


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