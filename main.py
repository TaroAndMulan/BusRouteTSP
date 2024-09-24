from os import statvfs
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from TSP_excel import CalculateRoutesExcel
from model import *
from database_operation import *
from form import *
import pandas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Connect to Postgres DB on supabase website
supabase  = connect_supabase()


@app.route('/')
def index():
    return redirect(url_for('home'))


#---------------------LOGIN/ LOGOUT/ REGISTER---------------------

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    user = GetUserFromDatabase(supabase,int(user_id))
    return dict_to_User(user)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email_supa(supabase, form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('อีเมลหรือรหัสผ่านไม่ถูกต้อง', 'danger')
    return render_template('login.html', form=form)
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    logout_user()
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        #if User.query.filter_by(email=email).first():
        #flash('อีเมลนี้ถูกลงทะเบียนแล้ว กรุณาเลือกอีเมลอื่น', 'danger')
        #return redirect(url_for('register'))
        hashed_password = generate_password_hash(form.password.data,
                                                 method='pbkdf2:sha256')
        new_user = User(user_id=0,
                        user_type=form.user_type.data,
                        name=form.name.data,
                        email=email,
                        phone=form.phone.data,
                        license=form.license.data
                        if form.user_type.data == 'driver' else None,
                        password=hashed_password)
        new_user = register_user(supabase, new_user)
        login_user(new_user)
        flash('สมัครสมาชิกสำเร็จ!', 'success')
        return redirect(url_for('index'))
    else:
        # Log the form errors
        flash('มีข้อผิดพลาดในการสมัครสมาชิก: {}'.format(form.errors), 'danger')
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    if not current_user:
        return redirect(url_for('login'))
    elif current_user.user_type == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('driver_dashboard'))

#---------------- DASHBOARD --------------------------#


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.user_type != 'admin':
        return redirect(url_for('home'))
    return render_template('admin_dashboard.html', user=current_user)


@app.route('/driver_dashboard')
@login_required
def driver_dashboard():
    if current_user.user_type != 'driver':
        return redirect(url_for('home'))
    return render_template('driver_dashboard.html', driver=current_user)


#---------------- CUSTOMERS--------------------------#

@app.route('/customer_list', methods=['GET'])
@login_required
def customer_list():
    search_query = request.args.get('search', '')
    customers = GetCustomersFromDatabase(supabase)
    if search_query:
        customers = [
            c for c in customers
            if search_query.lower() in (c["first_name"].lower() + " " +
                                        c["last_name"].lower())
        ]
    return render_template('customer_list.html',
                           customers=customers,
                           search_query=search_query)


@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = CustomerForm()

    if form.validate_on_submit():

        new_customer = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "address": form.address.data,
            "province": form.province.data,
            "phone": form.phone.data,
            "latitude": form.latitude.data,
            "longitude": form.longitude.data,
            "coordinate": form.coordinate.data
        }
        InsertCustomerToDatabase(supabase,new_customer)
        
        flash('เพิ่มลูกค้าเรียบร้อยแล้ว!', 'success')
        return redirect(url_for('customer_list'))
    return render_template('add_customer.html', form=form)


@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):

    form = CustomerForm()
    form.province.choices = [(i, p) for i, p in enumerate(get_provinces())]
    if form.validate_on_submit():
        edit_customer = {"first_name":form.first_name.data,
                        "last_name":form.last_name.data,
                        "address":form.address.data,
                         "province":form.province.data,
                        "phone":form.phone.data,
                        "latitude":form.latitude.data,
                        "longitude":form.longitude.data,
                        "coordinate":form.coordinate.data}
        EditCustomerInDatabase(supabase,int(customer_id),edit_customer)
        flash('อัปเดตข้อมูลลูกค้าเรียบร้อยแล้ว!', 'success')
        return redirect(url_for('customer_list'))
    return render_template('edit_customer.html', form=form, customer_id=customer_id)



@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
@login_required
def delete_customer(customer_id):
    DeleteCustomerInDatabase(supabase,customer_id)

    return redirect(url_for('customer_list'))


# ---------------------PRODUCTS-------------------------------------#

@app.route('/product_list', methods=['GET'])
@login_required
def product_list():
    products = GetProductFromDatabase(supabase)
    return render_template('product_list.html', products=products)
    

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = {
            "brand": form.brand.data,
            "weight_per_bag": form.weight_per_bag.data,
            "price": form.price.data
        }
        InsertProductToDatabase(supabase, new_product)        
        flash('เพิ่มสินค้าสำเร็จแล้ว!', 'success')
        return redirect(url_for('product_list'))
    return render_template('add_product.html', form=form)


@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    form = ProductForm()
    if form.validate_on_submit():
        edit_product = {'brand':form.brand.data,'weight_per_bag':form.weight_per_bag.data,'price':form.price.data}
        EditProductInDatabase(supabase,product_id,edit_product)
        flash('แก้ไขสินค้าสำเร็จแล้ว!', 'success')
        return redirect(url_for('product_list'))
    return render_template('edit_product.html',
                           form=form,
                           product_id=product_id)


@app.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    DeleteProductIndatabase(supabase,product_id)
    return redirect(url_for('product_list'))


# ---------------------MAP------------------------------------#


@app.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    return render_template('upload.html')



@app.route('/map_excel', methods= ['GET','POST'])
@login_required
def map_excel():
    file = request.files['file']
    df = pandas.read_excel(file,usecols="A:H")
    places = []
    coordinates = []
    data = []
    
    for index, row in df.iterrows():
        
        places.append(row['first_name'])
        coordinates.append((float(row['Latitude']),float(row['Longitude'])))

    route = CalculateRoutesExcel(places,coordinates)[1:-1]
    
    for r in route:
        customer_index = df[df['first_name'] == r].index[0]
        row = df.iloc[customer_index]
        data.append({
                       'first_name': str(row['first_name']),
                       'last_name': str(row['last_name']),
                       'address': str(row['address']),
                       'phone': str(row['phone']),
                       'latitude': float(row['Latitude']),
                       'longitude': float(row['Longitude'])
                   })
    sendMapToDatabase(supabase,data.copy())
    return render_template('map_excel.html',data=data)


@app.route('/map_driver', methods= ['GET','POST'])
@login_required
def map_driver():
    return render_template('map_excel.html',data=getMapFromDatabase(supabase)[0]['optimal'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
