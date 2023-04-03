from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


# from flask_login import LoginManager, login_required, logout_user, current_user





# from website import bcrypt

from . import db, bcrypt

# from flask import current_app
# bcrypt = current_app.bcrypt


from website.models import User
from . forms import RegistrationForm, LoginForm
from .models import User, Pizza, PizzaPrice, Topping, PizzaTopping, PizzaOrder, OrderHistory



auth = Blueprint('auth', __name__)





# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)



@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        output = 'Your account has been created! You are now able to log in'
    else:
        output = 'you tried but failed'
    return render_template('register.html', title='Register', form=form, output=output)






@auth.route("/oj", methods=['GET', 'POST'])
def oj():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # db.session.add(user)
        # db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        # return redirect(url_for('users.login'))
        output = 'Victory'
        return render_template('oj.html', title='OJ OJ OJ', form=form, output=output)
    else:
        output = form.username.data
    return render_template('oj.html', title='OJ OJ OJ', form=form, output=output)




@auth.route('/regTest', methods=['GET', 'POST'])
def regTest():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
    # else:
        # flash('Something went wrong!', 'success')
        flash('Something went wrong!')

    # Return the response for the authorized user
    return render_template('regTest.html', title='Register', form=form, no_sidebar=True)




# @auth.route('/regTest', methods=['GET', 'POST'])
# @login_required
# def regTest():
#     if current_user.id != 6:  # Replace 6 with the user_id you want to restrict access to
#         return redirect(url_for('views.home'))
#     else:
#         form = RegistrationForm()
#         if form.validate_on_submit():
#             hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#             user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#             db.session.add(user)
#             db.session.commit()
#             flash('Your account has been created! You are now able to log in', 'success')
#             message = 'Your account has been created! You are now able to log in'
#         else:
#             flash('Something went wrong!', 'success')
#             message = 'Please correct the errors below'

#         # Return the response for the authorized user
#         return render_template('regTest.html', title='Register', form=form, message=message)





# @auth.route('/regTest', methods=['GET', 'POST'])
# @login_required
# def regTest():
    
#         # Only the authenticated user can access this route
#     if current_user.id != 6:  # Replace 123 with the user_id you want to restrict access to
#         return redirect(url_for('views.home'))
#         # abort(403)  # Return a 403 Forbidden HTTP error code
#     else:
#         # Return the response for the authorized user
#         return render_template('regTest.html', user=current_user)

#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         message = 'Your account has been created! You are now able to log in'
#     else:
#         flash('Something went wrong!', 'success')
#         message = 'Please correct the errors below'
        
#     return render_template('regTest.html', title='Register', form=form, message=message)



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


# @auth.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('views.home'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('views.home'))
