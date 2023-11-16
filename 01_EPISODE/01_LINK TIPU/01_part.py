import requests
import random

url = 'https://uwuwiw.vrl2023.com/data.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    '''
    email: dsadsada
    sandi: dsadasdsadsadas
    login: Facebook
    '''
    # random of k
    k_random_email = random.randint(10, 20)
    k_random_sandi = random.randint(10, 250)
    
    # create random email
    random_email = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-', k=k_random_email)) + '@gmail.com'
    random_sandi = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-={}[]|:;'<>,.?/", k=k_random_sandi))
    
    data = {
        'email': random_email,
        'sandi': random_sandi,
        'login': 'Facebook'
    }
    response = requests.post(url, data=data, headers=headers)
    print("Successfully! with random : " + random_email+ " | "+ random_sandi)
    print(response.text)