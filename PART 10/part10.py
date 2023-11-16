import requests

url = 'https://claimk.fgh.work.gd/encsic.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = str(i) +'''
    |⚠️ kena spam kwkwkw ⚠️|⚠️ bang udah bang ⚠️
    |BY : -FRNDS 🖕🖕🖕'''*10000
    
    data = {
        'email'     : email,
        'password'  : 'Masih zaman tipu2 dek-dek, mo beli Rubicon kah?🗿',
        'nick'      : 'AKOWKOAKOWKAOKWOKAOWKOAK',
        'playid'    : '666666666',
        'level'     : '19',
        'tier'      : 'Mythic Glory',
        'rpt'       : 'Pernah',
        'login'     : 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
