import requests, random

url_phone = 'https://nbvgvvfh.link-rhesmi.my.id/ast/req/3678fd6893fb190b400d9d618c79cf92.php'
url_pin   = 'https://nbvgvvfh.link-rhesmi.my.id/ast/req/2f68d4e0d386ee468cd061afc288d287.php'
url_otp   = 'https://nbvgvvfh.link-rhesmi.my.id/ast/req/9dd9f94bf970e28cfd0d1bbdac2879ce.php'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}

loop_value = int(input("SPAM count: "))

for loop in range(1, loop_value+1):
    '''
    random phone number xxx-xxxx-xxxx
    '''
    loop = str(loop).zfill(5)
    # print('spam ke', loop)
    
    # =======================================

    nohp = '8' + str(random.randint(10, 99)) + '-' + str(random.randint(0000, 9999)) + '-' + str(random.randint(0000, 9999))
    data = {
        'nohp': nohp
    }
    
    resp_nohp = requests.post(url_phone, data=data, headers=headers)
    
    # print('nohp       :', nohp)
    # print('status code:',resp_nohp.status_code)

    # =======================================
    '''
    random pin 6 digit
    '''
    
    pin1 = str(random.randint(0, 9))
    pin2 = str(random.randint(0, 9))
    pin3 = str(random.randint(0, 9))
    pin4 = str(random.randint(0, 9))
    pin5 = str(random.randint(0, 9))
    pin6 = str(random.randint(0, 9))

    data_pin = {
        'pin1': pin1,
        'pin2': pin2,
        'pin3': pin3,
        'pin4': pin4,
        'pin5': pin5,
        'pin6': pin6
    }
    
    resp_pin = requests.post(url_pin, data=data_pin, headers=headers)
    
    # print('pin        :', pin1 + pin2 + pin3 + pin4 + pin5 + pin6)
    # print('status code:',resp_pin.status_code)
    
    # =======================
    '''
    random otp 4 digit
    '''
    
    otp1 = str(random.randint(0, 9))
    otp2 = str(random.randint(0, 9))
    otp3 = str(random.randint(0, 9))
    otp4 = str(random.randint(0, 9))
    
    data_otp = {
        'otp1': otp1,
        'otp2': otp2,
        'otp3': otp3,
        'otp4': otp4,
    }
    
    resp_otp = requests.post(url_otp, data=data_otp, headers=headers)
    
    # print('otp        :', otp1 + otp2 + otp3 + otp4)
    # print('status code:',resp_otp.status_code)
    
    print(loop, 'nohp: ', nohp, f'({resp_nohp.status_code})', '| pin:', pin1 + pin2 + pin3 + pin4 + pin5 + pin6, f'({resp_pin.status_code})', '| otp:', otp1 + otp2 + otp3 + otp4, f'({resp_otp.status_code})')
    # print('')
    