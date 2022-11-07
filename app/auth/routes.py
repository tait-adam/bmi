from flask import Blueprint, redirect, flash, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import RegistrationForm, LoginForm
from app import login_manager, db
from app.models import User

auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(
            db.select(User).filter_by(email=form.email.data)
        ).scalar()

        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Logged In')
            return redirect(next_page or url_for('charts.home'))
        flash('Invalid email/password combination')
        return redirect("/login")
    else:
        return render_template('login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Successfully logged-out')
    return redirect(url_for('auth.login'))


@auth.route("/register", methods=['GET', 'POST'])
def register():
    """User registration page"""
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = db.session.execute(
            db.select(User.id).filter_by(email=form.email.data)
        ).first()
        if existing_user is None:
            user = User(
                name=form.username.data,
                email=form.email.data,
                # TODO: select gender_id from genders table
                gender_id=1,
                birthday=form.birthday.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Congratulations. You have successfully registered')
            return redirect("/")
        flash('A user already exists with that email address')
        return redirect("/login")
    else:
        return render_template('register.html', form=form)


# Helper Functions
@login_manager.user_loader
def load_user(user_id):
    """Check is user is logged-in on every page load"""
    if user_id is not None:
        user = User.query.get(user_id)
        print(user)
        return user
        # TODO: Move away from query statement
        # return db.session.execute(
        #     db.select(User).filter_by(id=user_id)
        # ).first()
    return None


@login_manager.unauthorized_handler
def unauthorised():
    """Redirect unauthorised users to Login page"""
    flash('You must be logged-in to view that page')
    return redirect(url_for('auth.login'))
