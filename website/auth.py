from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Authentication routes are grouped in their own blueprint.
auth_bp = Blueprint('auth', __name__)


# Login checks the submitted email and password, then redirects safely.
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.email == email))
        if user is None:
            error = 'Incorrect email address'
        elif not check_password_hash(user.password_hash, password): # Compare stored hash with submitted password.
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') # Original protected URL, if login was required first.
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')


# Register creates a user after validating the form and hashing the password.
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():

        hashed_password = generate_password_hash(
            register_form.password.data
        ).decode('utf-8')

        user = User(
            first_name=register_form.first_name.data,
            surname=register_form.surname.data,
            email=register_form.email.data,
            contact_number=register_form.contact_number.data,
            street_address=register_form.street_address.data,
            password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash('Registration successful!')

        return redirect(url_for('auth.login'))

    return render_template(
        'user.html',
        form=register_form,
        heading='Register'
    )


# Logout clears the session and returns the user to the event list.
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
