from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from . import db
from .models import User
from .forms import RegisterForm

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("Email already registered. Please log in.")
            return redirect(url_for("login"))

        new_user = User(
            first_name=form.first_name.data,
            surname=form.surname.data,
            email=form.email.data,
            contact_number=form.contact_number.data,
            street_address=form.street_address.data,
            password_hash=generate_password_hash(form.password.data)
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)