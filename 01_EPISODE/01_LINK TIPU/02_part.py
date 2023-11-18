import requests
import random

url = 'https://jkwbdgskwj.tgwqb.my.id/data.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
loop_value = int(input("bar bar brp kali? : "))

for loop in range(1, loop_value+1):
    '''
    email: dasdasd
    sandi: dsadasdasdasd
    login: Facebook
    '''
    # random of k
    k_random_email = random.randint(10, 20)
    k_random_sandi = random.randint(10, 250)
    
    # create random email
    random_email = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789_.-', k=k_random_email)) + '@gmail.com'
    random_sandi = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-={}[]|:;'<>,.?/", k=k_random_sandi))
    
    data = {
        'email': random_email,
        'sandi': random_sandi,
        'login': 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print(f"{loop} | random email:" + random_email+ " | random sandi:"+ random_sandi)
    print(response.text)