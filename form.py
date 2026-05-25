from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    contact_number = StringField("Contact Number", validators=[DataRequired()])
    street_address = StringField("Street Address", validators=[DataRequired()])

    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6)
    ])

    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password", message="Passwords must match")
    ])

    submit = SubmitField("Register")