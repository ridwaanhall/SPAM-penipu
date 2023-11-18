import requests, random

url_phone = 'http://kerjabumn-com.preview-domain.com/req/phone.php'
url_otp_apk = 'http://kerjabumn-com.preview-domain.com/req/code.php' # 5 pin
url_otp_sms = 'http://kerjabumn-com.preview-domain.com/req/code2.php' # 6 pin

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}

loop_value = int(input("bar bar brp kali? : "))

for loop in range(1, loop_value+1):

    random_phoneNumber = '+62' + str(random.randint(100000000, 999999999))
    data = {
        'phoneNumber': random_phoneNumber
    }
    response = requests.post(url_phone, data=data, headers=headers)
    loop = str(loop).zfill(5)
    print(loop)
    print('phoneNumber:', random_phoneNumber)
    print(response.status_code)

    # =======================================

    random_pin1 = str(random.randint(0, 9))
    random_pin2 = str(random.randint(0, 9))
    random_pin3 = str(random.randint(0, 9))
    random_pin4 = str(random.randint(0, 9))
    random_pin5 = str(random.randint(0, 9))
    random_pin6 = str(random.randint(0, 9))

    data_otp = {
        'pin1': random_pin1,
        'pin2': random_pin2,
        'pin3': random_pin3,
        'pin4': random_pin4,
        'pin5': random_pin5,
        'pin6': random_pin6
    }
    
    response = requests.post(url_otp_sms, data=data_otp, headers=headers)
    print('pin:', random_pin1 + random_pin2 + random_pin3 + random_pin4 + random_pin5)
    # print('status code:',response.status_code)
    # print('cookies:',response.cookies)
    # print('', response.headers)
    # print(response.elapsed)
    # print(response.apparent_encoding)
    # print(response.close)
    # print(response.content)
    print('')
    