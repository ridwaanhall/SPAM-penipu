import requests
import random

# https://grp.mjquyw.com/o/?o=enwLmor
url = 'https://sskss.mujxk.com/data.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
loop_value = int(input("bar bar brp kali? : "))

for loop in range(1, loop_value+1):
    '''
    email: dsadasdas
    sandi: dsadasdasdad
    login: Facebook
    '''
    # random of k
    k_random_email = random.randint(10, 20)
    k_random_sandi = random.randint(10, 100)
    
    # create random email
    random_email = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789_.-', k=k_random_email)) + '@gmail.com'
    random_sandi = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-={}[]|:;'<>,.?/", k=k_random_sandi))
    
    data = {
        'email': random_email,
        'sandi': random_sandi*10000,
        'login': 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    # make loop in format 0000000001
    loop = str(loop).zfill(10)
    print(f"{loop}. " + random_email)
    print(response.text)