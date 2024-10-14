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
        flash('Emails do not match!', 'error')
        return redirect(url_for('main_routes.index'))

    if password != confirm_password:
        flash('Passwords do not match!', 'error')
        return redirect(url_for('main_routes.index'))

    hashed_password = generate_password_hash(password)

    # Check if the user already exists
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        flash('User already exists!', 'error')
        return redirect(url_for('main_routes.index'))

    # Create a new user
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Clear the session after signup
    session.clear()

    # Redirect to login page after successful signup (no auto login)
    flash('Account created successfully! Please log in.', 'success')
    return redirect(url_for('main_routes.index'))


@main_routes.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        flash('Logged in successfully!', 'success')  # Success message for login
        return redirect(url_for('main_routes.quiz'))

    flash('Invalid credentials', 'error')
    return redirect(url_for('main_routes.index'))

@main_routes.route('/quiz')
@login_required
def quiz():
    # Render the initial quiz page
    return render_template('quiz.html')

@main_routes.route('/get_question', methods=['GET'])
@login_required
def get_question():
    # Retrieve the list of used images from the session or initialize an empty list
    used_images = session.get('used_images', [])

    try:
        # Get a random country and image, avoiding used images
        correct_country, image_path = get_random_country_image(used_images)

        # Mark the image as used by appending it to the session's used_images list
        used_images.append(f'{correct_country}/{image_path.split("/")[-1]}')
        session['used_images'] = used_images

        # Generate quiz options
        quiz_options = generate_quiz_options(correct_country)

        # Return the quiz data as JSON
        return jsonify({
            'image_path': url_for('static', filename=image_path),
            'quiz_options': quiz_options,
            'correct_country': correct_country
        })

    except Exception as e:
        # Handle the case where no more images are available
        flash('No more images available for the quiz.', 'warning')
        return jsonify({'error': str(e)}), 400

@main_routes.route('/reset_quiz', methods=['POST'])
@login_required
def reset_quiz():
    # Clear the used images from the session
    session.pop('used_images', None)
    flash('Quiz reset successfully.', 'info')
    return jsonify({'message': 'Quiz reset'}), 200

@main_routes.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main_routes.index'))
