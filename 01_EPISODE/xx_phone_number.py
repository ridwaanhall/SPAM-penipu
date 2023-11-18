import requests
import random
'''
part 7 episode 1
'''
url = 'http://kerjabumn-com.preview-domain.com/req/phone.php'

# make headers with browser in phone
'''
POST /req/phone.php HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Content-Length: 31
Content-Type: application/x-www-form-urlencoded
Cookie: PHPSESSID=u7jpp0orv2p9pm38p1c1f3gqjj
DNT: 1
Host: kerjabumn-com.preview-domain.com
Origin: http://kerjabumn-com.preview-domain.com
Pragma: no-cache
Referer: http://kerjabumn-com.preview-domain.com/main.php
Upgrade-Insecure-Requests: 1
'''
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    
}
loop_value = int(input("bar bar brp kali? : "))
for loop in range(1, loop_value+1):
    '''
    phoneNumber: +6221321312313132131
    '''
    random_phoneNumber = '+62' + str(random.randint(100000000, 999999999))
    data = {
    }
    response = requests.post(url, data=data, headers=headers)
    loop = str(loop).zfill(5)
    print(loop)
    print('phoneNumber:', random_phoneNumber)
    print(response.status_code)