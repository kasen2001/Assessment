from . import db
from datetime import datetime
from flask_login import UserMixin


# User accounts own events, bookings, and comments.
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Relationships make it easy to load a user's created events and activity.
    my_events = db.relationship('Event', backref='creator', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)


# Event stores all public listing information and ticket availability.
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    venue_name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    artist_lineup = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)
    available_tickets = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open')
    acknowledgement_type = db.Column(db.String(50), nullable=False, default='No Acknowledgement')
    acknowledgement_text = db.Column(db.Text, nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Deleting an event also removes its dependent bookings and comments.
    bookings = db.relationship('Booking', backref='event', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='event', lazy=True, cascade='all, delete-orphan')


# Booking records a user's ticket purchase for one event.
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)


# Comment stores user feedback on an event detail page.
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
