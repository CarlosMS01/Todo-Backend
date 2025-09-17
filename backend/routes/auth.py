# backend/routes/auth.py
from flask import Blueprint, request, jsonify
from models import User
from database import db
from flask_bcrypt import Bcrypt
import jwt, os
from datetime import datetime, timedelta
from flask import make_response

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email ya registrado'}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado correctamente ✅'})


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')

    response = make_response(jsonify({'message': 'Login exitoso'}))
    response.set_cookie(
        'access_token',
        token,
        httponly=True,
        secure=True,         # solo se envía por HTTPS
        samesite='Strict',   # evita CSRF
        max_age=7200         # 2 horas
    )
    return response
