import requests

url = 'https://keibc.mtyx.my.id/check.php'

data = {
    'password': 'TOBAT BANGSAT',
    'playid': '111111111',
    'nickname': 'WKWKWKWKKWKW',
    'level': '100',
    'tier': 'Mythic Glory',
    'login': 'Moonton'
}

headers = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

for i in range(99999):
    email = 'toloooolll' + str(i+1) + '@modal.cok'
    data['email'] = email
    response = requests.post(url, data=data, headers=headers)
    print(f"penipu bi lek : bang udah bang {i+1}")
