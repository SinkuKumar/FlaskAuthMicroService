from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
db = SQLAlchemy(app)
jwt = JWTManager(app)

EMPLOYEE_DETAILS_API_URL = 'http://127.0.0.1:5001/profile'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'User already exists!'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password=hashed_password.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token), 200


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/profile', methods=['GET', 'POST'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    if request.method == 'GET':
        response = requests.get(f"{EMPLOYEE_DETAILS_API_URL}/{current_user}")
        return response.json(), response.status_code
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        contact_details = data.get('contact_details')
        address = data.get('address')
        emergency_contacts = data.get('emergency_contacts')

        payload = {
            'name': name,
            'contact_details': contact_details,
            'address': address,
            'emergency_contacts': emergency_contacts
        }

        response = requests.post(EMPLOYEE_DETAILS_API_URL, json=payload)

        if response.status_code == 201:
            return jsonify({'message': 'Employee details added successfully'}), 201
        else:
            return jsonify({'message': 'Failed to add employee details'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
