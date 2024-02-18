# Database.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float, ForeignKey
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class Admin(db.Model):
    __tablename__ = 'Admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    admin_data = [
        {'admin_id': 1, 'username': 'admin', 'password': '123'},
    ]

class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    residential_address = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Car(db.Model):
    __tablename__ = 'Car'
    car_id = db.Column(db.Integer, primary_key=True)
    car_name = db.Column(db.String(100), nullable=False)
    car_type = db.Column(db.String(50), nullable=False)
    car_brand = db.Column(db.String(50), nullable=False)
    transmission = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    hourly_rate = db.Column(Float, nullable=False)
    daily_rate = db.Column(Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, default=True)

    car_data = [
        {'car_id': 1, 'car_name': 'VIOS 1.3 J', 'car_type': 'Sedan', 'car_brand': 'Toyota', 'transmission': 'Manual',
        'color': 'Alumina Jade Metallic', 'hourly_rate': 104.17, 'daily_rate': 2500.00, 'quantity': 1},
        {'car_id': 2, 'car_name': 'COROLLA ALTIS 1.8 G GR-S', 'car_type': 'Sedan', 'car_brand': 'Toyota', 'transmission': 'Automatic',
        'color': 'Attitude Black Mica', 'hourly_rate': 104.17, 'daily_rate': 2500.00, 'quantity': 1},
        {'car_id': 3, 'car_name': 'CAMRY 2.5 V HEV', 'car_type': 'Sedan', 'car_brand': 'Toyota', 'transmission': 'Automatic',
        'color': 'Metal Stream Metallic', 'hourly_rate': 157.08, 'daily_rate': 3770.00, 'quantity': 1},
        {'car_id': 4, 'car_name': 'RAIZE 1.0 Turbo', 'car_type': 'Crossovers', 'car_brand': 'Toyota', 'transmission': 'Automatic',
        'color': 'White Pearl SE/Black', 'hourly_rate': 110.84, 'daily_rate': 2660.00, 'quantity': 1},
        {'car_id': 5, 'car_name': 'YARIS CROSS 1.5 S HEV', 'car_type': 'Crossovers', 'car_brand': 'Toyota', 'transmission': 'Automatic',
        'color': 'White Pearl / Attitude Black Mica', 'hourly_rate': 110.84, 'daily_rate': 2660.00, 'quantity': 1},
        {'car_id': 6, 'car_name': 'VELOZ 1.5 V', 'car_type': 'Crossovers', 'car_brand': 'Toyota', 'transmission': 'Automatic',
        'color': 'Purplish Silver Mica Metallic', 'hourly_rate': 110.84, 'daily_rate': 2660.00, 'quantity': 1},
        {'car_id': 7, 'car_name': 'FORTUNER 2.8 LTD 4x4', 'car_type': 'SUV', 'car_brand': 'Toyota', 'transmission': 'Automatic',
        'color': 'Silver Metallic/Attitude Black Mica', 'hourly_rate': 235.84, 'daily_rate': 5660.00, 'quantity': 1},
        {'car_id': 8, 'car_name': 'LAND CRUISER VX', 'car_type': 'SUV', 'car_brand': 'Toyota', 'transmission': 'Automatic',
        'color': 'Gray Metallic', 'hourly_rate': 479.17, 'daily_rate': 11500.00, 'quantity': 1},
        {'car_id': 9, 'car_name': 'SUPER GRANDIA Elite 2.8', 'car_type': 'Van', 'car_brand': 'Toyota', 'transmission': 'Automatic',
        'color': 'Gray Metallic', 'hourly_rate': 145.00, 'daily_rate': 2500.00, 'quantity': 1},
        {'car_id': 10, 'car_name': 'COMMUTER DELUXE 2.8L Diesel', 'car_type': 'Van', 'car_brand': 'Toyota', 'transmission': 'Manual',
        'color': 'Silver Mica Metallic', 'hourly_rate': 125.00, 'daily_rate': 1500.00, 'quantity': 1},
    ]