from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from functools import wraps
import os
import bcrypt
import datetime
import jwt
import re

# Init app
app = Flask(__name__)

import predictor_v2
import multi_prediction

# Database

# set configuration variables
DB_HOST = 'localhost'
DB_USERNAME = 'root'
DB_NAME = 'corn_i'

DB_MYSQL = f'mysql+pymysql://{DB_USERNAME}@{DB_HOST}:3306/{DB_NAME}'
DB_POSTGRES = f'postgresql://{DB_USERNAME}@{DB_HOST}:5432/{DB_NAME}'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_MYSQL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET'] = 'fd0a4496-12a5-4a57-9634-465ff719e7b6'


# Init DB
db = SQLAlchemy(app)
# Init Marshmallow (Marshmallow is a Python library that is often used in Flask applications for object serialization and deserialization.)
ma = Marshmallow(app)

# User Class/Model
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String(200), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)

  def __init__(self, email, password):
    self.email = email
    self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

  def check_password(self, password):
    return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

# User Schema For Serialization
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    

# Init schema
user_schema = UserSchema() # user_schema is used for serializing a single User object
users_schema = UserSchema(many=True) # users_schema is used for serializing a list of User objects


# Middleware
from functools import wraps
from flask import request, jsonify
import jwt

# Middleware Function
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        # Verify the token
        try:
            data = jwt.decode(token, app.config['JWT_SECRET'], algorithms=['HS256'])
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated



# Register Route
@app.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    password = request.json['password']
    
	# Check if email and password were provided
    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400
    
    # Check if email is valid
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'message': 'Invalid email address.'}), 400
    
    # Check if password is strong enough
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long.'}), 400
    if not any(char.isdigit() for char in password):
        return jsonify({'message': 'Password must contain at least one digit.'}), 400
    if not any(char.isupper() for char in password):
        return jsonify({'message': 'Password must contain at least one uppercase letter.'}), 400
    if not any(char.islower() for char in password):
        return jsonify({'message': 'Password must contain at least one lowercase letter.'}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409
    
    # Create new user
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    result = user_schema.dump(new_user)
    return jsonify({'message': 'User created successfully', 'user': result}), 201


# Login Route
@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    
	# Check if email and password were provided
    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400
    
    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    # Generate token with 3-hour expiration time
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    }
    token = jwt.encode(payload, app.config['JWT_SECRET'], algorithm='HS256')
    user_data = user_schema.dump(user)
    
    return jsonify({'token': token, 'user': user_data}), 200



# Protected Route
@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    user_data = user_schema.dump(current_user)
    return jsonify({'message': 'YOU HAVE VALID TOKEN. AUTHENTICATED', 'user': user_data}), 200


# Run Server
if __name__ == '__main__':
    app.run(debug=True)