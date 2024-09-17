from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

provinces_of_thailand = [
    "Bangkok", "Amnat Charoen", "Ang Thong", "Bueng Kan", "Buriram",
    "Chachoengsao", "Chai Nat", "Chaiyaphum", "Chanthaburi", "Chiang Mai",
    "Chiang Rai", "Chonburi", "Chumphon", "Kalasin", "Kamphaeng Phet",
    "Kanchanaburi", "Khon Kaen", "Krabi", "Lampang", "Lamphun", "Loei",
    "Lopburi", "Mae Hong Son", "Maha Sarakham", "Mukdahan", "Nakhon Nayok",
    "Nakhon Pathom", "Nakhon Phanom", "Nakhon Ratchasima", "Nakhon Sawan",
    "Nakhon Si Thammarat", "Nan", "Narathiwat", "Nong Bua Lamphu", "Nong Khai",
    "Nonthaburi", "Pathum Thani", "Pattani", "Phang Nga", "Phatthalung",
    "Phayao", "Phetchabun", "Phetchaburi", "Phichit", "Phitsanulok", "Phrae",
    "Phuket", "Prachinburi", "Prachuap Khiri Khan", "Ranong", "Ratchaburi",
    "Rayong", "Roi Et", "Sa Kaeo", "Sakon Nakhon", "Samut Prakan",
    "Samut Sakhon", "Samut Songkhram", "Saraburi", "Satun", "Sing Buri",
    "Sisaket", "Songkhla", "Sukhothai", "Suphan Buri", "Surat Thani", "Surin",
    "Tak", "Trang", "Trat", "Ubon Ratchathani", "Udon Thani", "Uthai Thani",
    "Uttaradit", "Yala", "Yasothon"
]


# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    user_type = SelectField('User Type',
                            choices=[('admin', 'Admin'), ('driver', 'Driver')],
                            validators=[DataRequired()])
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    license = StringField('License')
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(),
                                        EqualTo('password')])
    submit = SubmitField('Register')


class CustomerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    province = SelectField('Province', choices=provinces_of_thailand)
    phone = StringField('Phone', validators=[DataRequired()])
    latitude = StringField('Latitude')
    longitude = StringField('Longitude')
    coordinate = StringField('Coordinate')
    submit = SubmitField('Submit')


class ProductForm(FlaskForm):
    brand = StringField('Brand')
    weight_per_bag = FloatField('Weight Per Bag (kg)')
    price = FloatField('Price')
    submit = SubmitField('Submit')


class DeliveryForm(FlaskForm):
    user_id = SelectField('รายชื่อลูกค้า',
                          choices=[],
                          validators=[DataRequired()])

    submit = SubmitField('บันทึก')


"""
class DeliveryForm(FlaskForm):
    first_name = StringField('ชื่อ', validators=[DataRequired()])
    last_name = StringField('นามสกุล', validators=[DataRequired()])
    address = TextAreaField('ที่อยู่', validators=[DataRequired()])
    phone = StringField('โทรศัพท์', validators=[DataRequired()])
    submit = SubmitField('บันทึก')
"""
