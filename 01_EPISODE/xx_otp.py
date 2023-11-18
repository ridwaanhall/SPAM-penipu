import requests
import random
'''
part 7 episode 1
'''
url = 'http://kerjabumn-com.preview-domain.com/req/code.php'

# make headers with browser in phone
'''
Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding:
gzip, deflate
Accept-Language:
en-US,en;q=0.9
Cache-Control:
no-cache
Connection:
keep-alive
Content-Length:
33
Content-Type:
application/x-www-form-urlencoded
Cookie:
PHPSESSID=u7jpp0orv2p9pm38p1c1f3gqjj
Dnt:
1
Host:
kerjabumn-com.preview-domain.com
Origin:
http://kerjabumn-com.preview-domain.com
Pragma:
no-cache
Referer:
http://kerjabumn-com.preview-domain.com/main.php
Upgrade-Insecure-Requests:
1
'''
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}
loop_value = int(input("bar bar brp kali? : "))
for loop in range(1, loop_value+1):
    '''
    pin1: 1
    pin2: 2
    pin3: 3
    pin4: 2
    pin5: 1
    '''

    # make random pin from 0 to 9
    random_pin1 = str(random.randint(0, 9))
    random_pin2 = str(random.randint(0, 9))
    random_pin3 = str(random.randint(0, 9))
    random_pin4 = str(random.randint(0, 9))
    random_pin5 = str(random.randint(0, 9))
    
    data = {
        'pin1': random_pin1,
        'pin2': random_pin2,
        'pin3': random_pin3,
        'pin4': random_pin4,
        'pin5': random_pin5
    }
    response = requests.post(url, data=data, headers=headers)
    loop = str(loop).zfill(5)
    print(loop)
    print('pin:', random_pin1 + random_pin2 + random_pin3 + random_pin4 + random_pin5)
    # print status code
    print('status code :', response.status_code)