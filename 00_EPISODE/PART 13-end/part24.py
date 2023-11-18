import requests

url = 'https://btggb.ggkyyr1.biz.id/data.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = str(i) +'''
    |⚠️ kena sspam wkwkw ⚠️|⚠️ bang udah bang ⚠️ | CIE DATANYA DIHAPUS wkwkwk link baru
    |BY : -FRNDS 🖕🖕🖕'''*10000

    data = {
        'playid'    : '293821012',
        'level'     : '100',
        'tier'      : 'Master',
        'elitepass' : 'Pernah',
        'email'     : email,
        'password'  : 'Masih zaman tipu2 dek-dek, mo beli Rubicon kah?🗿',
        'login'     : 'Moonton'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
