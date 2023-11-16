
import requests

url = 'https://urubsy.codasssjh23.my.id/data.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = '|TOLOLLLL NGEPRANKk'* 10000 + str(i) + 'wkwk'
    
    data = {
        'playid'    : '6666666661',
        'nickname'  : 'RAMADHAN LHO BANGG',
        'level'     : '19',
        'tier'      : 'Mythic GloryY',
        'elitepass' : 'Pernah',
        'email'     : email,
        'password'  : 'TOBAT WOYYYYYY DASAR TITIT GA GUNA',
        'login'     : 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
