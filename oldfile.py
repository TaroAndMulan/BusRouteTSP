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


# Function to generate random Thai phone number
def generate_phone():
    return f"0{random.randint(60, 99)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"


# Function to generate random latitude and longitude within Thailand
def generate_coordinates():
    latitude = random.uniform(5.5, 20.5)  # Latitude range of Thailand
    longitude = random.uniform(97.5, 105.5)  # Longitude range of Thailand
    return latitude, longitude


def initialized_db(db):
    db['users'] = {}
    db['products'] = {}
    #db['customers'] = {}
    db['today_users'] = {}

    def hashedPassword(password):
        return generate_password_hash(password, method='pbkdf2:sha256')

    default_user_1 = User(1, 'admin', 'ADMIN', 'admin@example.com',
                          '1234567890', 'xx', hashedPassword('111111'))
    #default_user_2 = User(2, 'driver', 'mulan', 'd@example.com', '1234567890',
    # 'xx', hashedPassword('asdasd'))
    db['users'][default_user_1.user_id] = default_user_1.to_dict()
    #db['users'][default_user_2.user_id] = default_user_2.to_dict()
    defaultProduct = {
        'วาริช': {
            'weight_per_bag': 25,
            'price': 1050
        },
        'G-MAX': {
            'weight_per_bag': 10,
            'price': 1050
        },
        'GBP': {
            'weight_per_bag': 10,
            'price': 1200
        },
        'RTG': {
            'weight_per_bag': 20,
            'price': 1200
        },
        'TOTO': {
            'weight_per_bag': 25,
            'price': 915
        },
        'TRF': {
            'weight_per_bag': 25,
            'price': 1190
        }
    }
    i = 1
    for product in defaultProduct:
        db['products'][i] = {
            'id': i,
            'brand': product,
            'weight_per_bag': defaultProduct[product]['weight_per_bag'],
            'price': defaultProduct[product]['price']
        }
        i += 1

    # Generate random customer
    first_names = [
        "Anuwat", "Somchai", "Suwit", "Chaiwat", "Nattapong", "Arthit",
        "Saranya", "Kamon", "Kanokwan", "Supatra"
    ]
    last_names = [
        "Srisuk", "Chanthavong", "Thongsuk", "Wongthong", "Phongpanit",
        "Sukprasert", "Thanachai", "Chaisiri", "Rattanapong", "Sukjai"
    ]
    addresses = [
        "123 Moo 5, Tumbon Bangrak, Amphoe Mueang",
        "55/22 Soi Sukhumvit 31, Khlong Tan, Watthana",
        "888 Moo 3, Tumbon Nong Prue, Banglamung",
        "99/10 Banglamung Road, Pattaya City",
        "77/5 Soi Lat Phrao 101, Wang Thonglang",
        "45/7 Soi Ramkhamhaeng 24, Huamak, Bangkapi",
        "120/15 Moo 6, Tumbon Talat Yai, Amphoe Mueang",
        "210/55 Ratchaprarop Road, Makkasan, Ratchathewi",
        "150/3 Moo 2, Phahonyothin Road, Sai Mai",
        "555/18 Moo 4, Thung Song Hong, Lak Si",
        "60/14 Moo 12, Tumbon Bang Phra, Si Racha",
        "390/99 Moo 9, Sattahip Naval Base, Sattahip",
        "98/15 Moo 1, Tumbon Mae Hia, Mueang", "270/80 Moo 5, Bang Bo",
        "85/22 Moo 7, Tumbon Phraek Sa, Mueang",
        "510/17 Soi Ladprao 101, Khlong Chan, Bang Kapi",
        "11/89 Moo 6, Tumbon Klong Luang, Amphoe Klong Luang",
        "255/88 Ratchadapisek Road, Huai Khwang", "175/7 Moo 9, Tha Sala",
        "320/5 Moo 2, Tumbon Pak Nam, Mueang", "100/2 Moo 6, Tumbon Sala Dan",
        "250/3 Moo 8, Tumbon Pa Daet, Amphoe Mueang",
        "33/77 Moo 3, Tumbon Na Chom Thian, Sattahip",
        "99/13 Rattanathibet Road, Bang Yai",
        "88/10 Moo 4, Tumbon Mae Nam, Koh Samui"
    ]
    provinces = [
        "Chiang Rai", "Nakhon Pathom", "Samut Prakan", "Surat Thani", "Rayong",
        "Khon Kaen", "Nakhon Si Thammarat", "Lampang", "Udon Thani",
        "Kanchanaburi", "Phetchaburi", "Prachuap Khiri Khan", "Nakhon Sawan",
        "Phang Nga", "Trang", "Ayutthaya", "Lopburi", "Sukhothai", "Trat",
        "Ubon Ratchathani"
    ]

    # Generate 10 random customers
    for i in range(5):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        address = random.choice(addresses)
        province = random.choice(provinces)
        phone = generate_phone()
        latitude, longitude = generate_coordinates()
        coordinate = f"{latitude}, {longitude}"

        customer = Customer(i + 1, first_name, last_name, address, province,
                            phone, latitude, longitude, coordinate)
        db['customers'][customer.id] = customer.to_dict()


def get_provinces():
    provinces_of_thailand = [
        "Bangkok", "Amnat Charoen", "Ang Thong", "Bueng Kan", "Buriram",
        "Chachoengsao", "Chai Nat", "Chaiyaphum", "Chanthaburi", "Chiang Mai",
        "Chiang Rai", "Chonburi", "Chumphon", "Kalasin", "Kamphaeng Phet",
        "Kanchanaburi", "Khon Kaen", "Krabi", "Lampang", "Lamphun", "Loei",
        "Lopburi", "Mae Hong Son", "Maha Sarakham", "Mukdahan", "Nakhon Nayok",
        "Nakhon Pathom", "Nakhon Phanom", "Nakhon Ratchasima", "Nakhon Sawan",
        "Nakhon Si Thammarat", "Nan", "Narathiwat", "Nong Bua Lamphu",
        "Nong Khai", "Nonthaburi", "Pathum Thani", "Pattani", "Phang Nga",
        "Phatthalung", "Phayao", "Phetchabun", "Phetchaburi", "Phichit",
        "Phitsanulok", "Phrae", "Phuket", "Prachinburi", "Prachuap Khiri Khan",
        "Ranong", "Ratchaburi", "Rayong", "Roi Et", "Sa Kaeo", "Sakon Nakhon",
        "Samut Prakan", "Samut Sakhon", "Samut Songkhram", "Saraburi", "Satun",
        "Sing Buri", "Sisaket", "Songkhla", "Sukhothai", "Suphan Buri",
        "Surat Thani", "Surin", "Tak", "Trang", "Trat", "Ubon Ratchathani",
        "Udon Thani", "Uthai Thani", "Uttaradit", "Yala", "Yasothon"
    ]
    return provinces_of_thailand
