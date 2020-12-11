from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from Zoom import db, bcrypt
from Zoom.auth.forms import RegestrationForm, LoginForm
from Zoom.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegestrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, dept=form.dept.data, gender=form.gender.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account created Succefully, uou can now login :)', 'success')
        return redirect(url_for('auth.login'))
    return render_template("registre.html", title="Registre", form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if the user is logged in, don't show the page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # if the user isn't logged in
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # redirecting to the protected route
            next_page = request.args.get('next')
            flash(f'Welcome Back {current_user.username}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unseccessful, please check your Email and password', 'danger')
    return render_template("login.html",  title="Login", form=form)

@auth.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('auth.login'))