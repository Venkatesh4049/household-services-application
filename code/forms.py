from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')



class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('customer', 'Customer'), ('professional', 'Professional')], validators=[DataRequired()])
    submit = SubmitField('Register')



class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    base_price = StringField('Base Price', validators=[DataRequired()])
    submit = SubmitField('Create Service')



class ServiceRequestForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])
    remarks = StringField('Remarks')
    service_id = SelectField('Service', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Request Service')



class BlockApproveForm(FlaskForm):
    submit = SubmitField('Submit')