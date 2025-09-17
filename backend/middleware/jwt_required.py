# backend/middleware/jwt_required.py
from flask import request, jsonify
import jwt, os
from functools import wraps

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('access_token')  # ← ahora desde cookie

        if not token:
            return jsonify({'error': 'Token requerido'}), 401

        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401

        return f(*args, **kwargs)
    return wrapper
