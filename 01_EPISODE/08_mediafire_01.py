import requests, random, lorem
'''
list link :
005 FROM https://mediafire-new.my.id/mf/?p=987fe373 REDIRECT TO https://oeib.terbaiik.com/
006 https://rekbervwhwhdd.kepv.my.id/data.php
007 http://kerjabumn-com.preview-domain.com/req/code.php and http://kerjabumn-com.preview-domain.com/req/phone.php
008 https://fandobdvdgdf.kepv.my.id/index.php?aToken=verified redirect to https://fandobdvdgdf.kepv.my.id/data.php
https://ngjsks.mjusy.com/data.php
'''

url = 'https://ngjsks.mjusy.com/data.php'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
loop_value = int(input("input number of loop : "))

for loop in range(1, loop_value+1):
    '''
    email: qewqewqewq
    password: ewqewqewqewqewqeqw
    login: Facebook
    ...
    emailp: 21321ewqeq
    passwordq: dsadasdsadas
    login: Facebook
    ...
    pin1: 1
    pin2: 2
    pin3: 3
    pin4: 2
    pin5: 1
    phoneNumber: +6221321312313132131
    ...
    emailazantispam: 123123131
    passwordfarelcode: 23131312312
    login: Facebook
    ...
    email: qewqewqewq
    sandi: ewqewqewqewqewqeqw
    login: Facebook
    '''
    # random of k
    k_random_email = random.randint(10, 20)
    k_random_password = random.randint(10, 100)
    
    # create random email
    # random_email = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789_.-', k=k_random_email)) + '@gmail.com'
    # random_password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-={}[]|:;'<>,.?/", k=k_random_password))
    
    # random of lorem
    lorem_email = lorem.get_word() + '@' + lorem.get_word() + '.' + lorem.get_word()
    lorem_password = lorem.get_paragraph()
    
    data = {
        # random by ridwaanhall
        # 'email': random_email,
        # 'password': random_password*10000,
        # random by lorem
        # 'emailp': lorem_email,
        # 'passwordq': lorem_password*10000,
        # 'login': 'Facebook'
        'email': lorem_email,
        'sandi': lorem_password*10000,
        'login': 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    loop = str(loop).zfill(5)
    print('\n' + loop)
    print('email:', lorem_email)
    print(lorem_password)
    print('status code :', response.status_code)
    # print(response.text)