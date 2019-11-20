import requests

cred = {
    "email": "admin@gmail.com",
    "password": "admin"
}

login_url = 'http://localhost:5000/login'
api_url = 'http://localhost:5000/users'

res = requests.post(login_url, json=cred)
token = res.json().get('token')

if token:
    headers = {
        'Authorization': f'Bearer {token}'
    }

    res = requests.get(api_url, headers=headers)

    users = res.json()
    for user in users:
        print(user.get('email'))
else:
    print('No Token received, invalid login')
