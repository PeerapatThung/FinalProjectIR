from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

# @auth.route('/login')
# @cross_origin(origins=['http://localhost:3000'])
# def login():
#     return render_template('login.html')

@auth.route('/login', methods=['POST'])
@cross_origin(origins=['http://localhost:3000'])
def login_post():
    body = request.get_json()
    email = body['email']
    password = body['password']
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user and not check_password_hash(user.password, password):
        text = 'Please check your login details and try again.'
        return jsonify({'exist': text})

    login_user(user, remember=remember)
    return jsonify({'user': user.get_user()})

# @auth.route('/signup')
# @cross_origin(origins=['http://localhost:3000'])
# def signup():
#     return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
@cross_origin(origins=['http://localhost:3000'])
def signup_post():
    body = request.get_json()
    email = body['email']
    name = body['name']
    password = body['password']

    user = User.query.filter_by(email=email).first()

    if user:
        text = 'Email address already exists.'
        return jsonify({'exist': text})

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': 'Register Successful'})

@auth.route('/logout')
@cross_origin(origins=['http://localhost:3000'])
@login_required
def logout():
    logout_user()