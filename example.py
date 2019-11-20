import jwt

SECRET = 'secretkeyjwt'


def generate_token():
    data = {
        'user': 'Alex Purwoto',
        'admin': True
    }

    return jwt.encode(data, 'test', algorithm='HS256')


def validate_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms='HS256')
    except Exception as error:
        return False


def main():
    token = generate_token()
    is_valid = validate_token(token)

    print('Token is valid', is_valid)


main()
