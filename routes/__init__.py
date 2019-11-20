""" Routes """

from flask import jsonify, request
import jwt
from models import User
from app_core import app, db
from functools import wraps


def validate_token(request, is_admin=False):
    """ Token Test """
    # example auth header : Bearer token_kode
    auth_header = request.headers.get('Authorization')

    if not auth_header or 'Bearer ' not in auth_header:
        return {'message': 'Bad Authorization header'}

    split = auth_header.split(' ')

    if not len(split) == 2:
        return {'mesage': 'Bad Authorization header'}
    try:
        decode_data = jwt.decode(split[1], app.config['SECRET_KEY'])
        user = User.query.filter_by(
            public_id=decode_data.get('user_id')).first()

        if not user:
            return {'message': 'User not found'}

        if is_admin and not user.is_admin:
            return {'message': 'Not Admin token'}

        return {
            'message': 'User is authenticated',
            'user': user.as_dict()
        }

    except Exception as error:
        print(error)
        return {'mesage': 'Token is invalid'}


def token_required(is_admin=False):
    def token_required_inner(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            res = validate_token(request, is_admin)
            if not res.get('user'):
                return jsonify(res.get('message')), 401
            return f(res.get('user'), *args, **kwargs)
        return decorated
    return token_required_inner


@app.route("/")
def root():
    return jsonify({'message': 'API Root'})


@app.route("/login", methods=['POST'])
def login():
    """ Login User """
    try:
        req = request.get_json(silent=True)

        if not req or not req.get('email') or not req.get('password'):
            return jsonify({
                'message': 'No Login data found'
            })

        user = User.query.filter_by(email=req.get('email')).first()

        if user and user.check_password(req.get('password')):
            token_data = {
                'user_id': user.public_id
            }

            token = jwt.encode(token_data, app.config['SECRET_KEY'])

            return jsonify({'token': token.decode('UTF-8')})

        return jsonify({'message': 'Invalid Login'})

    except Exception as error:
        print(error)
        return jsonify({'message': 'Something went wrong'}), 400


@app.route("/users")
@token_required(is_admin=True)
def get_users(current_user):
    """ Get All User """

    data = User.query.all()

    users = [user.as_dict() for user in data]

    return jsonify(users)


@app.route("/user/<id>")
@token_required()
def api_get_user(current_user, id):
    """ Get one user with id """

    print(id)

    data = User.query.filter_by(public_id=id).first()

    return jsonify(data.as_dict())


@app.route("/users", methods=['POST'])
@token_required()
def add_user(current_user):
    """ Create new User """

    req = request.get_json(silent=True)
    if not req:
        return jsonify({
            'message': 'No JSON Data Found'
        })

    try:
        user = User(**req)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': f'User with id {user.public_id} created successfully',
            'data': user.as_dict()
        })
    except Exception as error:
        print(error)
        return jsonify({
            'message': 'Something went wrong',
        }), 400
