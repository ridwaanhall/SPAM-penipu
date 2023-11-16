import requests

url = 'https://btjrb.herexfonz.xyz/free-fire/checkAccount.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    userIdForm = "4666932100"+str(i)
    email      = str(i)+'AAANJING.BABI.KONTOL.MEMEK.JEBMBUT.TOLOLLL.BET.JADI.ORANG.WKWWKWK'*10000+'@gbapakkau.cok'
    password   = 'MMAKASIH SPAM BERHASIL '*10000+str(i)
    nickname   = 'Goblok lu anjeng Babi'+str(i)
    data = {
        'email'      : email,
        'password'   : password,
        'login'      : 'Facebook',
        'userIdForm' : userIdForm,
        'nickname'   : nickname,
        'lvl'        : 'Level 88',
        'rpt'        : 'Tidak Pernah',
        'rpl'        : 'Diamond'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
