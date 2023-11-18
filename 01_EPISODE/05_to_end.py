import requests
import random
'''
005 FROM https://mediafire-new.my.id/mf/?p=987fe373 REDIRECT TO https://oeib.terbaiik.com/
006 
'''
url = 'https://oeib.terbaiik.com/gcodeCheck.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
loop_value = int(input("input number of loop : "))

for loop in range(1, loop_value+1):
    '''
    email: qewqewqewq
    password: ewqewqewqewqewqeqw
    login: Facebook
    '''
    # random of k
    k_random_email = random.randint(10, 20)
    k_random_password = random.randint(10, 100)
    
    # create random email
    random_email = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789_.-', k=k_random_email)) + '@gmail.com'
    random_password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-={}[]|:;'<>,.?/", k=k_random_password))
    
    data = {
        'email': random_email,
        'password': random_password*10000,
        'login': 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    # make loop in format 0000000001
    loop = str(loop).zfill(5)
    print(f"{loop}. " + random_email)
    print(response.text)