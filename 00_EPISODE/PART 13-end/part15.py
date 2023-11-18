import requests

url = 'https://mso.qobx.my.id/BTG6ZO/data.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = str(i) +'''
    |⚠️ kena sspam wkwkw ⚠️|⚠️ bang udah bang ⚠️
    |BY : -FRNDS 🖕🖕🖕'''*10000

    data = {
        'playid'    : '666666666',
        'nickname'  : 'Pernah',
        'level'     : '100',
        'tier'      : 'Mythic Glory',
        'email'     : email,
        'password'  : 'Masih zaman tipu2 dek-dek, mo beli Rubicon kah?🗿',
        'login'     : 'Moonton'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
