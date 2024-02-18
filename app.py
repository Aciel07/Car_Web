'''
NomadRide Car Rental System, a web application that allows customers to rent cars and manage their profiles.
Users can sign up, log in, and log out.
The application uses Flask, SQLAlchemy, and Flask-Migrate.
The application has the following features:
1. Customer Profile Feature
2. Rent a Car Feature
3. Admin Dashboard
'''
from flask import Flask, flash, render_template, request, redirect, url_for, session
from models.database import db, Customer, Car, Admin
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "1231321"


migrate = Migrate(app, db)
db.init_app(app)

with app.app_context():
    # Create tables
    db.create_all()

    # Check if the Car table is empty
    if not db.session.query(Car.query.exists()).scalar():
        # Add initial data
        for car_info in Car.car_data:
            new_car = Car(**car_info)
            db.session.add(new_car)
    
    # Check if the Admin table is empty
    if not db.session.query(Admin.query.exists()).scalar():
        # Add initial admin data
        for admin_info in Admin.admin_data:
            new_admin = Admin(**admin_info)
            db.session.add(new_admin)

    db.session.commit()

# ------------------------------------------------------ [Main Menu] ------------------------------------------------------
# Index page
@app.route('/')
def index():
    return render_template('index.html')

# Main menu page
@app.route('/main_menu')
def main_menu():
    if 'username' in session:
        customers = Customer.query.all()
        return render_template('main_menu.html', username=session['username'], customers=customers)
    return redirect(url_for('index'))

# Login route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        # Query the database for the customer
        customer = Customer.query.filter_by(username=username, password=password).first()

        # Query the database for the admin
        admin = Admin.query.filter_by(username=username, password=password).first()

        if customer:
            session['username'] = username
            return redirect(url_for('main_menu'))
        elif admin:
            session['admin'] = username
            return redirect(url_for('admin'))

    # If login fails, redirect to the index page with an error message
    flash('Invalid username or password', 'error')
    return redirect(url_for('index'))


# sign_up route
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        # Check if the username already exists in the database
        existing_user = Customer.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('sign_up'))
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        residential_address = request.form.get('address')
        contact_number = request.form.get('contact_number')
        email = request.form.get('email')

        # Create a new customer
        new_customer = Customer(
            username=username, password=password, first_name=first_name,
            last_name=last_name, residential_address=residential_address,
            contact_number=contact_number, email=email
        )
        db.session.add(new_customer)
        db.session.commit()

        # Log in the new user
        session['username'] = username

        # Flash a success message
        flash('Sign up successful! You are now logged in.', 'success')

        # Redirect to the index page
        return redirect(url_for('index'))

    return render_template('sign_up.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# ------------------------------------------------------ [ADMIN] ------------------------------------------------------
# Admin route
@app.route('/admin/admin')
def admin():
    if 'admin' in session:
        users = Customer.query.all()
        cars = Car.query.all()
        return render_template('admin.html', admin='Admin', users=users, cars=cars)
    return redirect(url_for('index'))

# Remove user route
@app.route('/admin/remove_user', methods=['POST'])
def remove_user():
    if 'admin' in session:
        # Get username from the request
        username = request.json.get('username')

        # Query the user to be removed
        user_to_remove = Customer.query.filter_by(username=username).first()

        if user_to_remove:
            # Delete the user from the database
            db.session.delete(user_to_remove)
            db.session.commit()

            # Return a success message
            return flash ({'message': f'User {username} has been successfully removed.'}), 200
        else:
            # Return an error message if the user is not found
            return flash ({'message': f'User {username} not found.'}), 404

    # Return an error message if not an admin
    return flash ({'message': 'Unauthorized access.'}), 403

# Add car route
@app.route('/add_car', methods=['POST'])
def add_car():
    if request.method == 'POST':
        # Get car details from the form
        car_name = request.form['carName']
        car_type = request.form['carType']
        car_brand = request.form['carBrand']
        transmission = request.form['transmission']
        car_color = request.form['carColor']
        hourly_rate = float(request.form['hourlyRate'])
        daily_rate = float(request.form['dailyRate'])
        quantity = int(request.form['quantity'])
        availability = bool(int(request.form['availability']))

        # Create a new Car object
        new_car = Car(
            car_name=car_name,
            car_type=car_type,
            car_brand=car_brand,
            transmission=transmission,
            color=car_color,
            hourly_rate=hourly_rate,
            daily_rate=daily_rate,
            quantity=quantity,
            availability=availability
        )

        # Add the new car to the database
        db.session.add(new_car)
        db.session.commit()

        # Redirect to the admin dashboard
        return redirect(url_for('admin'))

    return redirect(url_for('index'))

# Remove car route
@app.route('/remove_car/<int:car_id>', methods=['POST'])
def remove_car(car_id):
    if 'admin' in session:
        # Query the car to be removed
        car_to_remove = Car.query.get(car_id)

        if car_to_remove:
            # Delete the car from the database
            db.session.delete(car_to_remove)
            db.session.commit()

            # Flash a success message
            flash(f'Car ID {car_id} has been successfully removed.', 'success')
        else:
            # Flash an error message if the car is not found
            flash(f'Car ID {car_id} not found.', 'error')

        # Redirect back to the admin dashboard
        return redirect(url_for('admin'))

    # Redirect to the index page if not an admin
    return redirect(url_for('index'))


# ------------------------------------------------------ [feature 1] Customer Profile Feature ------------------------------------------------------
# Profile route
@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        customer = Customer.query.filter_by(username=username).first()

        if customer:
            return render_template('profile.html', customer=customer)

    flash('You need to be logged in to access your profile.', 'info')
    return redirect(url_for('index'))

# Edit profile route
@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if 'username' in session:
        username = session['username']
        customer = Customer.query.filter_by(username=username).first()

        if customer:
            if request.method == 'POST':
                # Get the updated information from the form
                new_username = request.form.get('new_username', customer.username)
                new_residential_address = request.form.get('new_residential_address', customer.residential_address)
                new_email = request.form.get('new_email', customer.email)
                new_contact_number = request.form.get('new_contact_number', customer.contact_number)
                new_password = request.form.get('new_password')

                # Update the customer's information in the database
                customer.username = new_username
                customer.residential_address = new_residential_address
                customer.email = new_email
                customer.contact_number = new_contact_number

                # Update the password if a new one is provided
                if new_password:
                    customer.set_password(new_password)

                # Commit the changes to the database
                db.session.commit()

                # Flash a success message
                flash('Your profile has been updated successfully.', 'success')

                # Redirect to the profile page
                return redirect(url_for('profile'))

            # Redirect to the profile page if not a POST request
            return redirect(url_for('profile'))

    # Redirect to the index page if not logged in
    flash('You need to be logged in to edit your profile.', 'info')
    return redirect(url_for('index')) 

# Delete account route
@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' in session:
        username = session['username']
        customer = Customer.query.filter_by(username=username).first()

        if customer:
            
            # Delete customer
            db.session.delete(customer)
            db.session.commit()

            # Logout the user after account deletion
            session.pop('username', None)

            # Flash a success message
            flash('Your account has been successfully deleted.', 'success')

            # Redirect to the index page
            return redirect(url_for('index'))

    flash('You need to be logged in to delete your account.', 'info')
    return redirect(url_for('index'))

# ------------------------------------------------------ [feature 2] Rent a Car Feature ------------------------------------------------------
# rent_car route
@app.route('/rent_car', methods=['GET', 'POST'])
def rent_car():
    if request.method == 'POST':
        car_id = request.form.get('car_id')
        rent_type = request.form.get('rent_type')
        rent_duration = request.form.get('rent_duration')
        pickup_date_time = request.form.get('pickup_date_time')
        return_date_time = request.form.get('return_date_time')
        total_amount = request.form.get('total_amount')
        rent_confirmation = request.form.get('rent_confirmation')

        try:
            flash('Rental transaction successful!', 'success')
            return redirect(url_for('main_menu')) 
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    # Fetch cars from the database to display in the form
    cars = Car.query.all() 

    return render_template('rent_car.html', cars=cars)



if __name__ == '__main__':
    app.run(debug=True)