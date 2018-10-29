from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField, FieldList
from wtforms.validators import InputRequired, Length, AnyOf, Email
from collections import namedtuple
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = "My_secret"
bootstrap = Bootstrap(app)
#turn on/off CSRF
app.config['WTF_CSRF_ENABLED'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LezbGUUAAAAABTdZxarDM9PAHkul3o1eUj55DkY'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LezbGUUAAAAAK9Eqm8_NufHC3PpiHXKMkYi8_jT'
#this is for testing only, turns off recaptcha
app.config['TESTING'] = True
#time limit for CSRF form in seconds
#app.config['WTF_CSRF_TIME_LIMIT'] = 10

#Field Enclousers
class TelephoneForm(Form):
    country_code = IntegerField('country code')
    area_code = IntegerField('area code')
    number = StringField('number')

#Field Lists
class YearForm(Form):
    year = IntegerField('year')
    total = IntegerField('total')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required!'), Length(min=4, max=8, message="must be between 4 and 8 char")])
    password = PasswordField('password', validators=[InputRequired('A password is required'), AnyOf(values=['secret', 'word'])])
    age = IntegerField('age', default=24)
    true = BooleanField('true')
    email = StringField('email', validators=[Email()])
    home_phone = FormField(TelephoneForm)
    mobile_phone = FormField(TelephoneForm)
    years = FieldList(FormField(YearForm))
    recaptcha = RecaptchaField()

#form inheritance
class NameForm(LoginForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')


class User:
    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email
    
@app.route('/', methods=['GET', 'POST'])
def index():
    myuser = User('Dave', 42, 'dave.vineis@gmail.com')

    group = namedtuple('Group', ['year', 'total'])
    g1 = group(2005, 1000)
    g2 = group(2006, 1700)
    g3 = group(2007, 1500)

    years = {'years' : [g1,g2,g3]}

    form = NameForm(obj=myuser, data=years)

    #remove a form field if not needed by the user
    #del form.mobile_phone

    if form.validate_on_submit():
        #return '<h1>Username: {} Password: {} Age: {}</h1>'.format(form.username.data, form.password.data, form.age.data)

        output = '<h1>'

        for f in form.years:
            output += 'Year: {}'.format(f.year.data)
            output += 'Total: {} <br>'.format(f.total.data)
        output += '</h1>'

        return output
    
    return render_template('index.html', form=form)

@app.route('/dynamic', methods=['GET', 'POST'])
def dynamic():
    class DynamicForm(FlaskForm):
        pass
    
    DynamicForm.name = StringField('name')
    recaptcha = RecaptchaField()
    
    names = ['middle_name', 'last_name', 'nickname']
    
    for name in names:
        setattr(DynamicForm, name, StringField(name))
    form = DynamicForm()
    
    if form.validate_on_submit():
        return 'Form has been validated. Name: {}'.format(form.name.data)
    
    return render_template('dynamic.html', form=form, names=names)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)