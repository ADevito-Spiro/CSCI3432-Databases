from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import re
from decimal import Decimal
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'OFDS'

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'OFDS'

def connect_to_database():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')

        if email == 'admin@admin.com':
            session['logged_in'] = True 
            return redirect(url_for('handle_restaurant_action'))

        connection = connect_to_database()
        cursor = connection.cursor()

        query = "SELECT CustomerID FROM Customer WHERE CustomerEmail = %s"
        cursor.execute(query, (email,))
        customer_id = cursor.fetchone()

        if customer_id is not None:
            customer_id = customer_id[0]
            session['customer_id'] = customer_id
            connection.close()
            cursor.close()
            session['logged_in'] = True 
            return redirect(url_for('customer_home', customer_id=customer_id))
        else:
            connection.close()
            cursor.close()
            session.clear()
            return redirect(url_for('new_customer', email=email))

    return render_template('login.html')

@app.route('/restaurants', methods=['GET', 'POST'])
def get_restaurants():
    if request.method == 'POST':
        restaurant_id = request.form.get('restaurant_id')
        
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
        selected_item = request.form.get('selected_item')

        if not selected_item:
            flash("Please select a menu item.", "error")
            return redirect(url_for('menu', restaurant_id=restaurant_id))

        if 'cart' not in session:
            session['cart'] = []

        session['cart'].append(selected_item)
        print(session['cart'])
        flash("Order placed successfully!", "success")
        return redirect(url_for('view_cart', restaurant_id=restaurant_id))
        
    connection = connect_to_database()
    cursor = connection.cursor()

    session['restaurant_id'] = restaurant_id
    
    query = "SELECT RestaurantName FROM Restaurant WHERE RestaurantID = %s"
    cursor.execute(query, (restaurant_id,))
    restaurant_name = cursor.fetchone()[0]

    query = "SELECT MenuItem, MenuItemDesc, MenuItemPrice FROM Menu WHERE RestaurantID = %s"
    cursor.execute(query, (restaurant_id,))
    menu_items = cursor.fetchall()

    cursor.close()
    connection.close()
    return render_template('menu.html', restaurant_name=restaurant_name, menu_items=menu_items, restaurant_id=restaurant_id)

@app.route('/view_cart')
def view_cart():
    if 'cart' not in session:
        session['cart'] = []
    
    cart_items = session['cart']
    extracted_items = []

    for item in cart_items:
        match = re.match(r"\(\('(.*?)', '(.*?)', Decimal\('(.*?)'\)\),\)", item)
        if match:
            item_name = match.group(1)
            item_description = match.group(2)
            item_price = Decimal(match.group(3))
            extracted_items.append({'name': item_name, 'description': item_description, 'price': item_price})

    if 'customer_id' in session:
        connection = connect_to_database()
        cursor = connection.cursor()
    
        customer_id = session['customer_id']
            
        query = "SELECT CustomerName, CustomerEmail, CustomerAddress FROM Customer WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        name, email, address = cursor.fetchone()

        query = "SELECT * FROM PaymentInformation WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        payment_info = cursor.fetchone()

        # Check if the customer has payment information
        query = "SELECT * FROM PaymentInformation WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        payment_info = cursor.fetchone()
        has_payment_info = True if payment_info else False

        return render_template('cart.html', extracted_items=extracted_items, customer_id=customer_id, name=name, email=email, address=address, has_payment_info=has_payment_info, payment_info=payment_info)
    else:
        return render_template('cart.html', extracted_items=extracted_items)

@app.route('/add_payment_info', methods=['POST'])
def add_payment_info():
    card_number = request.form.get('card_number')
    card_name = request.form.get('card_name')
    card_expire_date = request.form.get('card_expire_date')
    card_ccn = request.form.get('card_ccn')

    connection = connect_to_database()
    cursor = connection.cursor()
    
    customer_id = session['customer_id']
    query = "Insert into PaymentInformation (CustomerID, CardNum, CardName, CardExpireDate, CardCCN) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (customer_id, card_number, card_name, card_expire_date, card_ccn))

    connection.commit()

    return redirect(url_for('view_cart'))

@app.route('/submit_order', methods=['POST'])
def submit_order():
    if request.method == 'POST':
        if 'cart' not in session:
            flash("Your cart is empty.", "error")
            return redirect(url_for('menu', restaurant_id=session.get('restaurant_id')))

        if 'customer_id' not in session:
            flash("Please log in to place an order.", "error")
            return redirect(url_for('login'))

        
        customer_id = session['customer_id']
        restaurant_id = session['restaurant_id']

        cart_items = session['cart']
        extracted_items = []

        for item in cart_items:
            match = re.match(r"\(\('(.*?)', '(.*?)', Decimal\('(.*?)'\)\),\)", item)
            if match:
                item_name = match.group(1)
                item_description = match.group(2)
                item_price = Decimal(match.group(3))
                extracted_items.append({'name': item_name, 'description': item_description, 'price': item_price})

        total_price = sum(item['price'] for item in extracted_items)

        connection = connect_to_database()
        cursor = connection.cursor()

        query = "INSERT INTO Orders (CustomerID, RestaurantID, OrdersDate, TotalPrice, OrdersStatus) VALUES (%s, %s, %s, %s, 'PENDING')"
        cursor.execute(query, (customer_id, restaurant_id, datetime.now(), total_price))

        order_id = cursor.lastrowid

        connection.commit()
        cursor.close()
        connection.close()

        session.pop('cart', None)
        session.pop('payment_info', None)

        flash("Order placed successfully! Your order number is {}".format(order_id), "success")
        return redirect(url_for('customer_home', customer_id=customer_id))
    else:
        return "Method Not Allowed", 405

@app.route('/customers', methods=['GET', 'POST'])
def new_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        payment_info = request.form['payment_info']

        connection = connect_to_database()
        cursor = connection.cursor()

        query = "Select COUNT(*) From Customer WHERE CustomerEmail = %s"
        cursor.execute(query, (email,))
        existing = cursor.fetchone()[0]

        if existing > 0:
            flash("An account already exists for this email")
            return render_template('customers.html')
        else:
            query = "INSERT INTO Customer (CustomerName, CustomerEmail, CustomerAddress, CustomerPaymentType) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, address, payment_info))

            connection.commit()

            customer_id=cursor.lastrowid

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

            query = "SELECT CustomerName FROM Customer WHERE CustomerID = %s"
            cursor.execute(query, (customer_id,))
            customer_name = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            return render_template('customer_home.html', customer_name=customer_name)

        except Exception as e:
            print("Error fetching recent orders:", e)
            return "Error fetching recent orders", 500
    else:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = "SELECT CustomerName FROM Customer WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        customer_name = cursor.fetchone()[0]

        query = "SELECT OrdersID FROM Orders WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        order_ids = cursor.fetchall()

        drivers = []
        order_dates = []
        total_prices = []

        for order_id in order_ids:
            driver_query = "SELECT DriverName, CurrentDriverLocation FROM Driver WHERE OrdersID = %s"
            cursor.execute(driver_query, (order_id,))
            driver_details = cursor.fetchone()
            drivers.append(driver_details)

            time_query = "SELECT OrdersDate FROM Orders WHERE OrdersID = %s"
            cursor.execute(time_query, (order_id,))
            time_of_order = cursor.fetchone()[0]
            order_dates.append(time_of_order)

            total_query = "SELECT TotalPrice FROM Orders WHERE OrdersID = %s"
            cursor.execute(total_query, (order_id,))
            total_cart = cursor.fetchone()[0]
            total_prices.append(total_cart)

        cursor.close()
        connection.close()

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

    cursor.execute("SELECT * FROM Customer WHERE CustomerID = %s", (customer_id,))
    customer = cursor.fetchone()

    cursor.close()
    connection.close()
    
    if customer:
        return redirect(url_for('customer_home', customer_id=customer_id))
    else:
        return "Customer not found", 404

@app.route('/edit_customer', methods=['GET'])
def edit_customers():
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT * FROM Customer"
    cursor.execute(query)
    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('edit_customer.html', customers=customers)

@app.route('/edit_single_customer', methods=['POST'])
def edit_single_customer():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        payment_info = request.form['payment_info']

        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            query = "Select COUNT(*) From Customer WHERE CustomerEmail = %s"
            cursor.execute(query, (email,))
            existing = cursor.fetchall()

            if existing > 0:
                flash("Account Already Exists with provided email")
                cursor.close()
                connection.close()
            else:
                query = "UPDATE Customer SET CustomerName = %s, CustomerEmail = %s, CustomerAddress = %s, CustomerPaymentType = %s WHERE CustomerID = %s"
                cursor.execute(query, (name, email, address, payment_info, customer_id))
                connection.commit()

                cursor.close()
                connection.close()

            return redirect(url_for('edit_customers')) 
        except Exception as e:
            print("Error updating customer data:", e)
            return "Error updating customer data", 500 
    else:
        return redirect(url_for('edit_customers'))

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    if request.method == 'POST':
        customer_id = request.form['customer_id']

        connection = connect_to_database()
        cursor = connection.cursor()

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

    query = "SELECT * FROM Restaurant"
    cursor.execute(query)
    restaurants = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('update_restaurant.html', restaurants=restaurants)

@app.route('/update_restaurant', methods=['POST'])
def update_single_restaurant():
    if request.method == 'POST':
        restaurant_id = request.form['restaurant_id']
        description = request.form['description']
        location = request.form['location']

        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            query = "UPDATE Restaurant SET RestaurantDesc = %s, RestaurantLocation = %s WHERE RestaurantID = %s"
            cursor.execute(query, (description, location, restaurant_id))
            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for('edit_restaurants'))
        except Exception as e:
            print("Error updating restaurant data:", e)
            return "Error updating restaurant data", 500 
    else:
        return redirect(url_for('edit_restaurants'))


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
            return "Invalid action", 400

        cursor.execute(query, (restaurant_id,))
        connection.commit()

    query_unapproved = "SELECT * FROM Restaurant WHERE Approved = FALSE"
    cursor.execute(query_unapproved)
    unapproved_restaurants = cursor.fetchall()

    query_all = "SELECT * FROM Restaurant WHERE Approved = TRUE"
    cursor.execute(query_all)
    all_restaurants = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('admin_restaurants.html', unapproved_restaurants=unapproved_restaurants, all_restaurants=all_restaurants)

@app.route('/clear')
def clear_session():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)