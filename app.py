from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_marshmallow.fields import fields
from marshmallow import pre_load
from functools import wraps
import bcrypt
import jwt
import re
import datetime


import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

# Init app
app = Flask(__name__)
CORS(app)

# Comment this import to remove prediction routes
import predictions


# Database

# set configuration variables
DB_MYSQL = f"mysql+pymysql://{os.getenv('DB_USERNAME')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
DB_POSTGRES = f"postgresql://{os.getenv('DB_USERNAME')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"


app.config['SQLALCHEMY_DATABASE_URI'] = DB_MYSQL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Init DB
db = SQLAlchemy(app)
# Init Marshmallow (Marshmallow is a Python library that is often used in Flask applications for object serialization and deserialization.)
ma = Marshmallow(app)

# User Class/Model
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String(200), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  created_at = db.Column(db.String(200), nullable=False, default=datetime.datetime.utcnow)


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
            data = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            current_user = User.query.filter_by(email=data['email']).first()
            if not current_user:
                raise ValueError('Token is invalid.')

        except ValueError as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated



# Register Route
@app.route('/register', methods=['POST'])
def register_user():
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
def login_user():
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
    token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')
    user_data = user_schema.dump(user)
    
    return jsonify({'token': token, 'user': user_data}), 200


# Get Current Login User Route
@app.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    user_data = user_schema.dump(current_user)
    return jsonify(user_data), 200

# Protected Route
@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    user_data = user_schema.dump(current_user)
    return jsonify({'message': 'YOU HAVE VALID TOKEN. AUTHENTICATED', 'user': user_data}), 200



# SoilTest Class/Model
class SoilTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farm_site = db.Column(db.String(200), nullable=False)
    client_name = db.Column(db.String(200), nullable=False)
    lab_no = db.Column(db.String(200), nullable=False)
    pH = db.Column(db.Float, nullable=False)
    P = db.Column(db.Float, nullable=False)
    K = db.Column(db.Float, nullable=False)
    N = db.Column(db.Float, nullable=False)
    MC = db.Column(db.Float, nullable=False)
    date_reported = db.Column(db.String(200), nullable=False, default=datetime.datetime.utcnow)
    created_at = db.Column(db.String(200), nullable=False, default=datetime.datetime.utcnow)



    def __init__(self, farm_site, client_name, lab_no, pH, P, K, N, MC, date_reported):
        self.farm_site = farm_site
        self.client_name = client_name
        self.lab_no = lab_no
        self.pH = pH
        self.P = P
        self.K = K
        self.N = N
        self.MC = MC
        self.date_reported = date_reported

# SoilTest Schema For Serialization
class SoilTestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SoilTest


# Init schema
soil_test_schema = SoilTestSchema() # soil_test_schema is used for serializing a single soil_test object
soil_tests_schema = SoilTestSchema(many=True) # soil_tests_schema is used for serializing a list of soil_test objects


# SoilTest Routes

# Create SoilTest Record
@app.route('/soiltest', methods=['POST'])
@token_required
def add_soiltest(current_user):
    try:
        # Check required fields
        required_fields = ['farm_site', 'client_name', 'lab_no', 'pH', 'P', 'K', 'N', 'MC', 'date_reported']
        fields_missing = []
        for field in required_fields:
            if field not in request.json:
                fields_missing.append(field)
        if fields_missing:
            raise ValueError(f'Missing required fields: {fields_missing}')

        # Check field values
        if not isinstance(request.json['pH'], float):
            raise ValueError('pH must be a floating point number')
        if not isinstance(request.json['P'], int):
            raise ValueError('P must be an integer')
        if not isinstance(request.json['K'], int):
            raise ValueError('K must be an integer')
        if not isinstance(request.json['N'], int):
            raise ValueError('N must be an integer')
        if not isinstance(request.json['MC'], float):
            raise ValueError('MC must be a floating point number')
    except ValueError as e:
        # Return validation error as JSON response
        return jsonify({'error': str(e)}), 400

    # Create new soiltest object
    soiltest = SoilTest(
        farm_site=request.json['farm_site'],
        client_name=request.json['client_name'],
        lab_no=request.json['lab_no'],
        pH=request.json['pH'],
        P=request.json['P'],
        K=request.json['K'],
        N=request.json['N'],
        MC=request.json['MC'],
        date_reported=request.json['date_reported']
    )
    
    db.session.add(soiltest)
    db.session.commit()

    
    # Serialize the soiltest object
    result = soil_test_schema.dump(soiltest)

    return soil_test_schema.jsonify(result)


# Get All SoilTest Records
@app.route('/soiltests', methods=['GET'])
@token_required
def get_soiltests(current_user):
    soiltests = SoilTest.query.all()
    result = soil_tests_schema.dump(soiltests)
    return jsonify(result)


# Update SoilTest Record
@app.route('/soiltest/<int:id>', methods=['PUT'])
@token_required
def update_soiltest(current_user, id):
    soiltest = SoilTest.query.get(id)
    if soiltest:
        try:
            # Check field values
            if 'pH' in request.json and not isinstance(request.json['pH'], float):
                raise ValueError('pH must be a floating point number')
            if 'P' in request.json and not isinstance(request.json['P'], int):
                raise ValueError('P must be an integer')
            if 'K' in request.json and not isinstance(request.json['K'], int):
                raise ValueError('K must be an integer')
            if 'N' in request.json and not isinstance(request.json['N'], int):
                raise ValueError('N must be an integer')
            if 'MC' in request.json and not isinstance(request.json['MC'], float):
                raise ValueError('MC must be a floating point number')
        except ValueError as e:
            # Return validation error as JSON response
            return jsonify({'error': str(e)}), 400
        
        # Update soiltest object
        soiltest.farm_site = request.json.get('farm_site', soiltest.farm_site)
        soiltest.client_name = request.json.get('client_name', soiltest.client_name)
        soiltest.lab_no = request.json.get('lab_no', soiltest.lab_no)
        soiltest.pH = request.json.get('pH', soiltest.pH)
        soiltest.P = request.json.get('P', soiltest.P)
        soiltest.K = request.json.get('K', soiltest.K)
        soiltest.N = request.json.get('N', soiltest.N)
        soiltest.MC = request.json.get('MC', soiltest.MC)
        soiltest.date_reported = request.json.get('date_reported', soiltest.date_reported)
        
        db.session.commit()

        # Serialize the updated soiltest object
        result = soil_test_schema.dump(soiltest)

        return soil_test_schema.jsonify(result)
    else:
        return jsonify({'error': 'SoilTest record not found'}), 404


# Delete SoilTest Record
@app.route('/soiltest/<int:id>', methods=['DELETE'])
@token_required
def delete_soiltest(current_user, id):
    soiltest = SoilTest.query.get(id)
    if soiltest:
        db.session.delete(soiltest)
        db.session.commit()
        return jsonify({'message': 'SoilTest record deleted successfully', 'id': id})
    else:
        return jsonify({'error': 'SoilTest record not found'}), 404


@app.route('/soiltests/<int:num>', methods=['GET'])
def get_latest_soiltest(num):
    farm_site = request.args.get('farm_site')
    if farm_site:
        soiltests = SoilTest.query.filter(SoilTest.farm_site == farm_site).order_by(SoilTest.date_reported.desc()).limit(num).all()
    else:
        soiltests = SoilTest.query.order_by(SoilTest.date_reported.desc()).limit(num).all()
    result = soil_tests_schema.dump(soiltests)
    return jsonify(result)


@app.route('/soiltests/latest', methods=['GET'])
def get_single_latest_soiltest():
    farm_site = request.args.get('farm_site')
    if farm_site:
        soiltest = SoilTest.query.filter(SoilTest.farm_site == farm_site).order_by(SoilTest.date_reported.desc()).first()
    else:
        soiltest = SoilTest.query.order_by(SoilTest.date_reported.desc()).first()
    result = soil_test_schema.dump(soiltest)
    return jsonify(result)



# Run Server
if __name__ == '__main__':
    app.run(debug=True)