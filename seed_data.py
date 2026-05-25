from website import create_app, db
from website.models import User, Event, Booking, Comment
from flask_bcrypt import generate_password_hash
from datetime import date, time, datetime

app = create_app()

with app.app_context():
    # Clear existing data
    Comment.query.delete()
    Booking.query.delete()
    Event.query.delete()
    User.query.delete()

    # Sample users
    user1 = User(
        first_name='Ichiro',
        surname='Yamaguchi',
        email='ichiro@sakanaction.com',
        password_hash=str(generate_password_hash('password123')),
        contact_number='0412345678',
        street_address='Meguro-ku, Tokyo'
    )

    user2 = User(
        first_name='Satoru',
        surname='Iguchi',
        email='satoru@kinggnu.com',
        password_hash=str(generate_password_hash('password456')),
        contact_number='0498765432',
        street_address='88 Queen Street, Brisbane'
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Sample music festival events
    event1 = Event(
        title='Brisbane Summer Sound Festival',
        description='A full-day outdoor music festival featuring local bands, food trucks, and summer vibes.',
        date=date(2026, 7, 18),
        start_time=time(12, 0),
        end_time=time(22, 0),
        venue_name='Riverstage Brisbane',
        city='Brisbane',
        image='Brisbane_for_207group.jpg',
        genre='Pop',
        artist_lineup='Luna Bay, The Riverlights, DJ Nova',
        price=89.00,
        total_tickets=500,
        available_tickets=480,
        status='Open',
        acknowledgement_type='Generic Acknowledgement',
        acknowledgement_text='We acknowledge the Traditional Custodians of the land on which this event takes place and pay our respects to Elders past and present.',
        creator_id=user1.id
    )

    event2 = Event(
        title='Neon EDM Night',
        description='An energetic night festival with EDM performances, light shows, and dance music.',
        date=date(2026, 8, 8),
        start_time=time(18, 0),
        end_time=time(23, 30),
        venue_name='Fortitude Music Hall',
        city='Brisbane',
        image='Night_fes_for_207group.jpg',
        genre='EDM',
        artist_lineup='DJ Pulse, Neon Wave, SkyDrop',
        price=75.00,
        total_tickets=300,
        available_tickets=0,
        status='Sold Out',
        acknowledgement_type='No Acknowledgement',
        acknowledgement_text=None,
        creator_id=user1.id
    )

    event3 = Event(
        title='J-Pop Festival',
        description='An exciting J-pop festival with food trucks.',
        date=date(2026, 9, 12),
        start_time=time(13, 0),
        end_time=time(21, 0),
        venue_name='Roma Street Parkland',
        city='Brisbane',
        image='Japan_for_207group.jpg',
        genre='J-pop',
        artist_lineup='King Gnu, Sakanaction, Fujii Kaze, Kenshi Yonezu',
        price=55.00,
        total_tickets=250,
        available_tickets=230,
        status='Open',
        acknowledgement_type='Enhanced Acknowledgement',
        acknowledgement_text='This event recognises the Traditional Custodians of the Brisbane area and encourages visitors to learn about the continuing connection between First Nations peoples and Country.',
        creator_id=user2.id
    )

    db.session.add_all([event1, event2, event3])
    db.session.commit()

    # Sample booking
    booking1 = Booking(
        quantity=2,
        total_price=178.00,
        booking_date=datetime.now(),
        user_id=user2.id,
        event_id=event1.id
    )

    # Sample comment
    comment1 = Comment(
        comment_text='This festival looks amazing! I am excited for the lineup.',
        created_at=datetime.now(),
        user_id=user2.id,
        event_id=event1.id
    )

    db.session.add(booking1)
    db.session.add(comment1)
    db.session.commit()

    print('Sample data added successfully.')