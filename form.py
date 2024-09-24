from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo


provinces_of_thailand = [
    'กรุงเทพมหานคร', 'สมุทรปราการ', 'นนทบุรี', 'ปทุมธานี', 'พระนครศรีอยุธยา',
    'อ่างทอง', 'ลพบุรี', 'สิงห์บุรี', 'ชัยนาท', 'สระบุรี', 'ชลบุรี', 'ระยอง',
    'จันทบุรี', 'ตราด', 'ฉะเชิงเทรา', 'ปราจีนบุรี', 'นครนายก', 'สระแก้ว',
    'นครราชสีมา', 'บุรีรัมย์', 'สุรินทร์', 'ศรีสะเกษ', 'อุบลราชธานี',
    'ยโสธร', 'ชัยภูมิ', 'อำนาจเจริญ', 'หนองบัวลำภู', 'ขอนแก่น', 'อุดรธานี',
    'เลย', 'หนองคาย', 'มหาสารคาม', 'ร้อยเอ็ด', 'กาฬสินธุ์', 'สกลนคร',
    'นครพนม', 'มุกดาหาร', 'เชียงใหม่', 'ลำพูน', 'ลำปาง', 'อุตรดิตถ์',
    'แพร่', 'น่าน', 'พะเยา', 'เชียงราย', 'แม่ฮ่องสอน', 'นครสวรรค์',
    'อุทัยธานี', 'กำแพงเพชร', 'ตาก', 'สุโขทัย', 'พิษณุโลก', 'พิจิตร',
    'เพชรบูรณ์', 'ราชบุรี', 'กาญจนบุรี', 'สุพรรณบุรี', 'นครปฐม', 'สมุทรสาคร',
    'สมุทรสงคราม', 'เพชรบุรี', 'ประจวบคีรีขันธ์', 'นครศรีธรรมราช', 'กระบี่',
    'พังงา', 'ภูเก็ต', 'สุราษฎร์ธานี', 'ระนอง', 'ชุมพร', 'สงขลา', 'สตูล',
    'ตรัง', 'พัทลุง', 'ปัตตานี', 'ยะลา', 'นราธิวาส'
]

def get_provinces():
    return provinces_of_thailand
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

