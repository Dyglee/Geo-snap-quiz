from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from app.utils import get_random_country_image, generate_quiz_options

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    return render_template('base.html')

@main_routes.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    confirm_email = request.form['confirm-email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    # Validate email and password
    if email != confirm_email:
        flash('Emails do not match!')
        return redirect(url_for('main_routes.index'))

    if password != confirm_password:
        flash('Passwords do not match!')
        return redirect(url_for('main_routes.index'))

    hashed_password = generate_password_hash(password)

    # Check if the user already exists
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        flash('User already exists!')
        return redirect(url_for('main_routes.index'))

    # Create a new user
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Explicitly clear the session after signup
    session.clear()

    # Redirect to login page after successful signup (no auto login)
    flash('Account created successfully! Please log in.')
    return redirect(url_for('main_routes.index'))


@main_routes.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('main_routes.quiz'))

    flash('Invalid credentials')
    return redirect(url_for('main_routes.index'))

@main_routes.route('/quiz')
@login_required
def quiz():
    correct_country, image_path = get_random_country_image()
    
    # Step 2: Generate quiz options
    quiz_options = generate_quiz_options(correct_country)
    
    # Render the quiz page with the image and options
    return render_template('quiz.html', image_path=image_path, quiz_options=quiz_options, correct_country=correct_country)

@main_routes.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('main_routes.index'))
