from os import statvfs
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from replit import db
import json
from model import *
from database_operation import *
from form import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize Replit database with some value
initialized_db(db)


# Login Manager
@login_manager.user_loader
def load_user(user_id):
    return get_user(db, user_id)


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email(db, form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('อีเมลหรือรหัสผ่านไม่ถูกต้อง', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        #if User.query.filter_by(email=email).first():
        #flash('อีเมลนี้ถูกลงทะเบียนแล้ว กรุณาเลือกอีเมลอื่น', 'danger')
        #return redirect(url_for('register'))
        hashed_password = generate_password_hash(form.password.data,
                                                 method='pbkdf2:sha256')
        new_user = User(user_id=len(db.get("users", {})) + 1,
                        user_type=form.user_type.data,
                        name=form.name.data,
                        email=email,
                        phone=form.phone.data,
                        license=form.license.data
                        if form.user_type.data == 'driver' else None,
                        password=hashed_password)
        db['users'][new_user.user_id] = new_user.to_dict()
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
    #return redirect(url_for('register'))
    if not current_user:
        return redirect(url_for('login'))
    elif current_user.user_type == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('driver_dashboard'))


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


@app.route('/customer_list', methods=['GET'])
@login_required
def customer_list():
    search_query = request.args.get('search', '')
    customers = get_customers(db)
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
        add_customer_todb(db,
                          first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          address=form.address.data,
                          province=form.province.data,
                          phone=form.phone.data,
                          latitude=form.latitude.data,
                          longitude=form.longitude.data,
                          coordinate=form.coordinate.data)
        flash('เพิ่มลูกค้าเรียบร้อยแล้ว!', 'success')
        return redirect(url_for('customer_list'))
    return render_template('add_customer.html', form=form)


@app.route('/edit_customer/<string:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    customers = db.get("customers", {})
    customer = customers.get(customer_id)
    if not customer:
        return "Customer not found", 404
    form = CustomerForm()
    form.province.choices = [(i, p) for i, p in enumerate(get_provinces())]
    if form.validate_on_submit():
        print("is IN form")
        customer = Customer(id=customer_id,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            address=form.address.data,
                            province=form.province.data,
                            phone=form.phone.data,
                            latitude=form.latitude.data,
                            longitude=form.longitude.data,
                            coordinate=form.coordinate.data)
        db["customers"][customer_id] = customer.to_dict()
        flash('อัปเดตข้อมูลลูกค้าเรียบร้อยแล้ว!', 'success')
        return redirect(url_for('customer_list'))
    return render_template('edit_customer.html', form=form, customer=customer)


@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
@login_required
def delete_customer(customer_id):
    customers = db.get("customers", {})
    print("wii", customers)
    if str(customer_id) in customers:
        print(type(customer_id))
        del customers[str(customer_id)]
        flash('ลบลูกค้าเรียบร้อยแล้ว!', 'success')
    else:
        flash('ไม่พบลูกค้า', 'danger')
    return redirect(url_for('customer_list'))


@app.route('/product_list', methods=['GET'])
@login_required
def product_list():
    products = db.get("products", {}).values()
    #print(db.get("products"))
    return render_template('product_list.html', products=products)


@app.route('/map', methods=['GET'])
@login_required
def map():
    return render_template('map.html')


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product_id = random.randint(100, 10000000)
        new_product = {
            "id": product_id,
            "brand": form.brand.data,
            "weight_per_bag": form.weight_per_bag.data,
            "price": form.price.data
        }
        db["products"][product_id] = new_product
        flash('เพิ่มสินค้าสำเร็จแล้ว!', 'success')
        return redirect(url_for('product_list'))
    return render_template('add_product.html', form=form)


@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    form = ProductForm()
    if form.validate_on_submit():
        db.get("products")[str(product_id)]['brand'] = form.brand.data
        db.get("products")[str(
            product_id)]['weight_per_bag'] = form.weight_per_bag.data
        db.get("products")[str(product_id)]['price'] = form.price.data
        flash('แก้ไขสินค้าสำเร็จแล้ว!', 'success')
        return redirect(url_for('product_list'))
    return render_template('edit_product.html',
                           form=form,
                           product_id=product_id)


@app.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    del db.get("products")[str(product_id)]
    return redirect(url_for('product_list'))


@app.route('/delivery_list', methods=['GET'])
@login_required
def delivery_list():
    deliveries = db.get("deliveries", {}).values()
    return render_template('delivery_list.html', deliveries=deliveries)


@app.route('/today_deliveries', methods=['GET', 'POST'])
@login_required
def today_deliveries():
    today_customer = db.get("customers", {}).values()
    return render_template('today_deliveries.html', customers=today_customer)


@app.route('/add_delivery', methods=['GET', 'POST'])
@login_required
def add_delivery():
    customers = get_customers(db)
    choices = [
        (c["id"],
         c["first_name"] + " " + c['last_name'] + ",     " + c['province'])
        for c in customers
    ]
    form = DeliveryForm()
    form.user_id.choices = choices
    if form.validate_on_submit():
        flash('อัปเดตข้อมูลการจัดส่งเรียบร้อยแล้ว!', 'success')
        return redirect(url_for('delivery_list'))
    return render_template('add_delivery.html', form=form)


@app.route('/edit_delivery/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def edit_delivery(delivery_id):
    deliveries = db.get("deliveries", {})
    delivery = deliveries.get(delivery_id)
    if not delivery:
        return "Delivery not found", 404
    form = DeliveryForm(obj=delivery)
    if form.validate_on_submit():
        delivery.update({
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "address": form.address.data,
            "phone": form.phone.data
        })
        db["deliveries"][delivery_id] = delivery
        flash('อัปเดตข้อมูลการจัดส่งเรียบร้อยแล้ว!', 'success')
        return redirect(url_for('delivery_list'))
    return render_template('edit_delivery.html', form=form, delivery=delivery)


@app.route('/delete_delivery/<int:delivery_id>', methods=['POST'])
@login_required
def delete_delivery(delivery_id):
    deliveries = db.get("deliveries", {})
    if delivery_id in deliveries:
        del deliveries[delivery_id]
        db["deliveries"] = deliveries
        flash('ลบข้อมูลการจัดส่งเรียบร้อยแล้ว!', 'success')
    else:
        flash('ไม่พบข้อมูลการจัดส่ง', 'danger')
    return redirect(url_for('delivery_list'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
