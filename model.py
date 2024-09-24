#--------------------------------------------------------------
# PRODUCT MODEL
#--------------------------------------------------------------

class Product:
  def __init__(self,id,brand,weight_per_bag,price):
    self.id = id
    self.brand = brand
    self.weight_per_bag = weight_per_bag
    self.price = price

#--------------------------------------------------------------
# CUSTOMER MODEL
#--------------------------------------------------------------

class Customer:
  def __init__(self, id, first_name, last_name, address, province, phone, latitude, longitude, coordinate):
      self.id = id
      self.first_name = first_name
      self.last_name = last_name
      self.address = address
      self.province = province
      self.phone = phone
      self.latitude = latitude
      self.longitude = longitude
      self.coordinate = coordinate
      self.today = False
    # Method to convert class attributes to a dictionary
  def to_dict(self):
    return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "province": self.province,
            "phone": self.phone,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "coordinate": self.coordinate,
            "today":self.today
    }

#--------------------------------------------------------------
# USER MODEL
#--------------------------------------------------------------
class User:
  def __init__(self, user_id, user_type, name, email, phone, license,
           password):
      self.user_id = user_id
      self.user_type = user_type
      self.name = name
      self.email = email
      self.phone = phone
      self.license = license
      self.password = password
  # Method to convert the User object to a dictionary
  def to_dict(self):
      return {
          "user_id": self.user_id,
          "user_type": self.user_type,
          "name": self.name,
          "email": self.email,
          "phone": self.phone,
          "license": self.license,
          "password": self.password
      }

  def get_id(self):
      return str(self.user_id)

  def is_active(self):
      return True

  def is_anonymous(self):
      return False

  def is_authenticated(self):
      return True
#----------------------------------------------------
