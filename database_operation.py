from model import *
from werkzeug.security import generate_password_hash
import random


def dict_to_User(user_dict):
    return User(user_id=user_dict["user_id"],
                user_type=user_dict["user_type"],
                name=user_dict["name"],
                email=user_dict["email"],
                phone=user_dict["phone"],
                license=user_dict["license"],
                password=user_dict["password"])


"""
def add_product(db,id,brand,weight_per_bag,price):
    product = Product(id,brand,weight_per_bag,price)
    db["products"][id] = product
"""


def add_user(db, user_type, name, email, phone, license, password):
    user_id = len(db.get("users", {})) + 1
    user = {
        "id": user_id,
        "user_type": user_type,
        "name": name,
        "email": email,
        "phone": phone,
        "license": license,
        "password": password
    }
    db.setdefault("users", {})[user_id] = user
    return user


def get_user(db, user_id):
    try:
        return dict_to_User(db['users'][str(user_id)])
    except:
        return dict_to_User(db['users'][str(1)])


def get_user_by_email(db, email):
    for user in db['users'].values():
        if user['email'] == email:
            return dict_to_User(user)
    return {}


def add_customer_todb(db, first_name, last_name, address, province, phone,
                      latitude, longitude, coordinate):
    customer_id = random.randint(100, 10000000)
    customer = {
        "id": customer_id,
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "province": province,
        "phone": phone,
        "latitude": latitude,
        "longitude": longitude,
        "coordinate": coordinate
    }
    db["customers"][customer_id] = customer


def get_products(db):
    return db.get("products", {}).values()


def edit_product(db, brand, weight_per_bag, price):
    for product in db['products'].values():
        if product['brand'] == brand:
            product['weigth_per_bag'] = weight_per_bag
            product['price'] = price


def get_customers(db):
    return db.get("customers", {}).values()


def get_provinces_in_db(db):
    return db.get("provinces", {}).values()


def add_province(db, name):
    province_id = len(db.get("provinces", {})) + 1
    province = {"id": province_id, "name": name}
    db.setdefault("provinces", {})[province_id] = province
    return province


# Function to generate random latitude and longitude within Thailand
def generate_coordinates():
    latitude = random.uniform(5.5, 20.5)  # Latitude range of Thailand
    longitude = random.uniform(97.5, 105.5)  # Longitude range of Thailand
    return latitude, longitude

def hashedPassword(password):
    return generate_password_hash(password, method='pbkdf2:sha256')

def initialized_db(db):
    if len(db['users'])==0:
        db['users'] = {}
        
    if len(db['products']) == 0:
        db['products'] = {}

    if len(db['customers']) == 0:
        db['customers'] = {}







