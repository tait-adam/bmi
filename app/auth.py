from flask import Blueprint, redirect, flash, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import RegistrationForm, LoginForm
from app import login_manager, db
from app.models import User, Gender

user = Blueprint(
    'user',
    __name__
)


@user.route("/login", methods=['GET', 'POST'])
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
            # TODO: validate value of next with is_safe_url(next)
            flash('Successfully logged-in')
            return redirect(next_page or url_for('charts.home'))
        flash('Invalid email/password combination')
        return redirect("/login")
    else:
        return render_template('login.html', form=form)


@user.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Successfully logged-out')
    return redirect(url_for('user.login'))


@user.route("/register", methods=['GET', 'POST'])
def register():
    """User registration page"""
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = db.session.execute(
            db.select(User.id).filter_by(email=form.email.data)
        ).first()
        if existing_user is None:
            gender_id = db.session.execute(
                db.select(Gender.id).filter_by(biology=form.gender.data)
            ).scalar()
            user = User(
                name=form.username.data,
                email=form.email.data,
                gender_id=gender_id,
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
        return db.session.execute(
            db.select(User).filter_by(id=user_id)
        ).scalar()
    return None


@login_manager.unauthorized_handler
def unauthorised():
    """Redirect unauthorised users to Login page"""
    flash('You must be logged-in to view that page')
    return redirect(url_for('user.login'))
