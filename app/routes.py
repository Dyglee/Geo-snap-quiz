from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main_routes.quiz'))  # Redirect to quiz if logged in
    return render_template('base.html')

@main_routes.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    session['user_id'] = new_user.id

    return redirect(url_for('main_routes.quiz'))

@main_routes.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('main_routes.quiz'))

    return jsonify({'error': 'Invalid credentials'}), 400

@main_routes.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')