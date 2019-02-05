from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField, FieldList
from wtforms.validators import InputRequired, Length, AnyOf, Email, ValidationError
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

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required!'), Length(min=4, max=8, message="must be between 4 and 8 char")])
    password = PasswordField('password', validators=[InputRequired('A password is required'), AnyOf(values=['secret', 'word'])])
    recaptcha = RecaptchaField()
    
    #create custom validation errors
    def validate_username(form, field):
        if field.data != 'Dave':
            raise ValidationError("You have the wrong username")

    
@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    user = User(username='dave', password='password')
    print(user.username)
    print(user.password)
    if form.validate_on_submit():
        form.populate_obj(user)
        print(user.username)
        print(user.password)
        return 'Form Submitted'
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)