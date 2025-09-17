import requests
url = ("https://api.github.com/users?per_page=5")
reponse = requests.get(url).json()
for users in reponse:
    print(f"login {reponse[1] ['login']}")
    print(f'avatar url: {reponse[0]['avatar_url']}')
