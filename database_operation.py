from model import *
from werkzeug.security import generate_password_hash
from supabase import create_client, Client


#--------------Connect_to_database---------------------------------------
def connect_supabase():
    url = "https://cyfvhiygtkpljtmkvcbw.supabase.co"
    key = ""
    supabase: Client = create_client(url, key)
    return supabase



#--------------- USERS-----------------------
def GetUserFromDatabase(db,user_id):
    response = (
        db.table("users")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    return response.data[0]

def createUserFromDict(user_dict):
    return User(user_id=user_dict["user_id"],
                user_type=user_dict["user_type"],
                name=user_dict["name"],
                email=user_dict["email"],
                phone=user_dict["phone"],
                license=user_dict["license"],
                password=user_dict["password"])


def get_user_by_email_supa(db,email):
    response = db.from_('users').select('*').eq("email", email).single().execute()
    return createUserFromDict(response.data)

def register_user(db,User):
    response = (db.table("users").insert({
        "user_type": User.user_type, "name": User.name, "email": User.email, "phone": User.phone,"license": User.license, "password": User.password}).execute()
               )
    return createUserFromDict(response.data[0])

def dict_to_User(user_dict):
    return User(user_id=user_dict["user_id"],
                user_type=user_dict["user_type"],
                name=user_dict["name"],
                email=user_dict["email"],
                phone=user_dict["phone"],
                license=user_dict["license"],
                password=user_dict["password"])

#--------------- Customer------------------------------

    
def InsertCustomerToDatabase(db,customer):
    response = (
        db.table("customers")
        .insert(customer)
        .execute()
    )
def EditCustomerInDatabase(db,customer_id,customer):
    response = (
        db.table("customers")
        .update(customer)
        .eq("id", customer_id)
        .execute()
    )
def DeleteCustomerInDatabase(db,customer_id):
    response = db.table('customers').delete().eq('id', customer_id).execute()
    
def get_customer_byID(db, customer_id):
    return db["customers"][str(customer_id)]

def GetCustomersFromDatabase(db):
    response = (
        db.table("customers")
        .select("*")
        .execute()
    )
    return response.data
    
def get_products(db):
    return db.get("products", {}).values()

def GetProductFromDatabase(db):
    response = (
        db.table("products")
        .select("*")
        .execute()
    )
    return response.data
    
def InsertProductToDatabase(db,product):
    response = (
        db.table("products")
        .insert(product)
        .execute()
    )

def EditProductInDatabase(db,product_id,product):
    response = (
        db.table("products")
        .update(product)
        .eq("id", product_id)
        .execute()
    )

def DeleteProductIndatabase(db,product_id):
    response = db.table('products').delete().eq('id', product_id).execute()


#--------------- PRODUCTS------------------------------

    
def edit_product(db, brand, weight_per_bag, price):
    for product in db['products'].values():
        if product['brand'] == brand:
            product['weigth_per_bag'] = weight_per_bag
            product['price'] = price

#--------------- UTILITY------------------------------

def hashedPassword(password):
    return generate_password_hash(password, method='pbkdf2:sha256')


#--------------- PRODUCTS------------------------------
def sendMapToDatabase(db,routes):  
    response = (
        db.table("route")
        .insert({"optimals":routes,"optimal":routes})
        .execute()
    )

def getMapFromDatabase(db):
    response = (
        db.table("route")
        .select("optimal")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return response.data