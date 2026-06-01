import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Event, Booking, Comment
from .forms import EventForm, BookingForm, CommentForm
from . import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    search = request.args.get('search', '').strip()
    genre = request.args.get('genre', '').strip()
    city = request.args.get('city', '').strip()

    query = Event.query
    if search:
        query = query.filter(Event.title.ilike(f'%{search}%'))
    if genre:
        query = query.filter(Event.genre.ilike(f'%{genre}%'))
    if city:
        query = query.filter(Event.city.ilike(f'%{city}%'))

    events = query.all()
    return render_template('index.html', events=events, search=search, genre=genre, city=city)


@main_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    booking_form = BookingForm()
    comment_form = CommentForm()
    return render_template('event_detail.html', event=event,
                           booking_form=booking_form, comment_form=comment_form)


@main_bp.route('/event/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        image_filename = 'default.jpg'
        if form.image.data and form.image.data.filename:
            f = form.image.data
            filename = secure_filename(f.filename)
            upload_dir = os.path.join(os.path.dirname(__file__), 'static', 'image')
            f.save(os.path.join(upload_dir, filename))
            image_filename = filename
        elif not form.image.data or not form.image.data.filename:
            flash('Please upload an event image.')
            return render_template('event_create.html', form=form)

        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            venue_name=form.venue_name.data,
            city=form.city.data,
            genre=form.genre.data,
            artist_lineup=form.artist_lineup.data,
            price=float(form.price.data),
            total_tickets=form.total_tickets.data,
            available_tickets=form.total_tickets.data,
            status=form.status.data,
            acknowledgement_type=form.acknowledgement_type.data,
            acknowledgement_text=form.acknowledgement_text.data or None,
            creator_id=current_user.id,
            image=image_filename,
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('main.event_detail', event_id=event.id))

    return render_template('event_create.html', form=form)


@main_bp.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.creator_id != current_user.id:
        abort(403)

    form = EventForm(obj=event)
    if form.validate_on_submit():
        already_booked = sum(b.quantity for b in event.bookings)
        if form.total_tickets.data < already_booked:
            flash(f'Cannot reduce total tickets below the number already booked ({already_booked}).')
            return render_template('event_edit.html', form=form, event=event)

        if form.image.data and form.image.data.filename:
            f = form.image.data
            filename = secure_filename(f.filename)
            upload_dir = os.path.join(os.path.dirname(__file__), 'static', 'image')
            f.save(os.path.join(upload_dir, filename))
            event.image = filename

        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.venue_name = form.venue_name.data
        event.city = form.city.data
        event.genre = form.genre.data
        event.artist_lineup = form.artist_lineup.data
        event.price = float(form.price.data)
        event.total_tickets = form.total_tickets.data
        event.available_tickets = max(0, form.total_tickets.data - already_booked)
        event.status = form.status.data
        event.acknowledgement_type = form.acknowledgement_type.data
        event.acknowledgement_text = form.acknowledgement_text.data or None

        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('main.event_detail', event_id=event.id))

    return render_template('event_edit.html', form=form, event=event)


@main_bp.route('/event/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.creator_id != current_user.id:
        abort(403)

    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.')
    return redirect(url_for('main.index'))


@main_bp.route('/event/<int:event_id>/book', methods=['POST'])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = BookingForm()

    if form.validate_on_submit():
        quantity = form.quantity.data

        if event.status != 'Open':
            flash('This event is not available for booking.')
            return redirect(url_for('main.event_detail', event_id=event_id))

        if quantity > event.available_tickets:
            flash(f'Only {event.available_tickets} ticket(s) remaining.')
            return redirect(url_for('main.event_detail', event_id=event_id))

        booking = Booking(
            quantity=quantity,
            total_price=round(quantity * event.price, 2),
            user_id=current_user.id,
            event_id=event_id,
        )
        event.available_tickets -= quantity
        if event.available_tickets == 0:
            event.status = 'Sold Out'

        db.session.add(booking)
        db.session.commit()
        flash(f'Successfully booked {quantity} ticket(s) for {event.title}!')
    else:
        flash('Invalid booking request. Please enter a valid quantity.')

    return redirect(url_for('main.event_detail', event_id=event_id))


@main_bp.route('/event/<int:event_id>/comment', methods=['POST'])
@login_required
def add_comment(event_id):
    Event.query.get_or_404(event_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            comment_text=form.comment_text.data,
            user_id=current_user.id,
            event_id=event_id,
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted!')
    else:
        flash('Could not post comment. Please try again.')

    return redirect(url_for('main.event_detail', event_id=event_id))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    my_events = Event.query.filter_by(creator_id=current_user.id).order_by(Event.date.asc()).all()
    return render_template('dashboard.html', bookings=bookings, my_events=my_events)


@main_bp.route('/support')
def support():
    return render_template('support.html')
