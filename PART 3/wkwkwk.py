import requests

url = 'http://paoos.duckdns.org/data.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = 'TOLOLLLL NGeeEPRANK' + str(i) + '''GW TUTORIN DEK?
    MINIMAL NGERTI BATASAN LAH''' * 10000
    
    data = {
        'playid': '666666666',
        'nickname': 'RAMADHAN LHO BANG',
        'level': '19',
        'tier': 'Mythic Glory',
        'email': email,
        'password': 'TOBAT WOYYYY DASAR TITIT GA GUNA',
        'login': 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
