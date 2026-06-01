from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import (
    TextAreaField, SubmitField, StringField, PasswordField,
    SelectField, IntegerField, DecimalField, DateField, TimeField
)
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, Optional


# Login form validates the two fields needed for existing users.
class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[
        InputRequired(),
        Email("Please enter a valid email")
    ])
    password = PasswordField("Password", validators=[
        InputRequired('Enter user password')
    ])
    submit = SubmitField("Login")


# Registration form collects the user profile and confirms the password.
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired(), Email("Please enter a valid email")])
    contact_number = StringField("Contact Number", validators=[InputRequired()])
    street_address = StringField("Street Address", validators=[InputRequired()])
    password = PasswordField("Password", validators=[
        InputRequired(),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Register")


# Event form is shared by the create and edit event pages.
class EventForm(FlaskForm):
    title = StringField("Event Title", validators=[InputRequired(), Length(max=150)])
    description = TextAreaField("Description", validators=[InputRequired()])
    date = DateField("Date", validators=[InputRequired()])
    start_time = TimeField("Start Time", validators=[InputRequired()])
    end_time = TimeField("End Time", validators=[InputRequired()])
    venue_name = StringField("Venue Name", validators=[InputRequired(), Length(max=150)])
    city = StringField("City", validators=[InputRequired(), Length(max=80)])
    genre = StringField("Genre", validators=[InputRequired(), Length(max=50)])
    artist_lineup = TextAreaField("Artist Lineup", validators=[InputRequired()])
    price = DecimalField("Ticket Price ($)", places=2, validators=[InputRequired(), NumberRange(min=0)])
    total_tickets = IntegerField("Total Tickets", validators=[InputRequired(), NumberRange(min=1)])
    status = SelectField("Status", choices=[
        ('Open', 'Open'),
        ('Inactive', 'Inactive'),
        ('Cancelled', 'Cancelled'),
        ('Sold Out', 'Sold Out'),
    ])
    acknowledgement_type = SelectField("Acknowledgement Type", choices=[
        ('No Acknowledgement', 'No Acknowledgement'),
        ('Generic Acknowledgement', 'Generic Acknowledgement'),
        ('Enhanced Acknowledgement', 'Enhanced Acknowledgement'),
    ])
    acknowledgement_text = TextAreaField("Acknowledgement Text", validators=[Optional()])
    image = FileField("Event Image", validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField("Save Event")


# Booking form limits each booking request to a small ticket quantity.
class BookingForm(FlaskForm):
    quantity = IntegerField("Number of Tickets", validators=[
        InputRequired(),
        NumberRange(min=1, max=10, message="Please enter between 1 and 10 tickets.")
    ])
    submit = SubmitField("Book Now")


# Comment form keeps event discussion messages short.
class CommentForm(FlaskForm):
    comment_text = TextAreaField("Comment", validators=[
        InputRequired(),
        Length(max=500, message="Comment cannot exceed 500 characters.")
    ])
    submit = SubmitField("Post Comment")
