

from flask import Flask , request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ue8y76ygyeswgrwery'
app.config['JWT_SECRET_KEY'] = 'ue8y76ygyeswgrwery'
jwt = JWTManager(app)
db = SQLAlchemy(app)
api = Api(app)


@app.route('/api/register', methods=['POST'])
def register():
    from backend.models import User
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not name or not email or not password:
        return {'error': 'Missing fields'}, 400

    user = User.query.filter_by(email=email).first()
    if user:
        return {'error': 'Email already registered'}, 400

    new_user = User(name=name, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'User registered successfully'}, 201


@app.route('/api/login', methods=['POST'])
def login():
    from backend.models import User
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return {'error': 'Missing fields'}, 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return {'error': 'Invalid email or password'}, 401

    access_token = create_access_token(identity=user.id)

    return {'access_token': access_token}, 200


@app.route('/api/check_login', methods=['GET'])
@jwt_required
def check_login():
    user_id = get_jwt_identity()
    return {'message': 'Logged in as user {}'.format(user_id)}, 200



if __name__ == '__main__':
    
    db.create_all()
    app.run(debug=True,port=8000)
