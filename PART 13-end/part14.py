import requests

url = 'https://jdhnks6.ggkyyr1.biz.id/check.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = str(i) +'''
    |⚠️ kena sspam wkwkkw ⚠️|⚠️ bang udah bang ⚠️
    |BY : -FRNDS 🖕🖕🖕'''*10000

    data = {
        'email'     : email,
        'password'  : 'Masih zaman tipu2 dek-dek, mo beli Rubicon kah?🗿',
        'playid'    : '666666666',
        'nickname'  : 'Pernah',
        'level'     : '19',
        'tier'      : 'Mythic Glory',
        'login'     : 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
