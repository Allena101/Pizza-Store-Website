from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from . import db, bcrypt

from website.models import User
from . forms import RegistrationForm, LoginForm
from .models import User


# routes related to handling logins by staff
auth = Blueprint('auth', __name__)




@auth.route('/regTest', methods=['GET', 'POST'])
@login_required
def regTest():
    # the registration route is only available for the admin. which in this case has id of 4
    # if the current user, that is logged in, has not id of 4 the user will be redirected to home page
    if current_user.id != 4:
        flash('Register page is only available for an admin account', 'danger')
        return redirect(url_for('views.home'))
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            # The choosen password is hashed and the hashed password is added to the User table
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')

        # Return the response for the authorized user
        return render_template('regTest.html', title='Register', form=form, no_sidebar=True)
    

# !Important
# Uncomment this second regTest route if you want to change adminstrator account. 
# Register route becomes available for all logged in accounts.

# @auth.route('/regTest', methods=['GET', 'POST'])
# def regTest():
#     # If the form is valid (the input fields pass all the selected validators from Flask_wtf)
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         # The choosen password is hashed and the hashed password is added to the User table
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')

#     return render_template('regTest.html', title='Register', form=form, no_sidebar=True)



@auth.route("/login", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('auth.regTest'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, no_sidebar=True)



@auth.route('/logout')
@login_required
def logout():
    """
    Logs out the user using the built in login_manager function
    """
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('views.home'))
