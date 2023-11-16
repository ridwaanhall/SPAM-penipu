import requests

url = 'https://btjrb.herexfonz.xyz/free-fire/verification.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email      = str(i)+'AAANJING.BABI.KONTOL.MEMEK.JEBMBUT.TOLOLLL.BET.JADI.ORANG.WKWWKWK'*10000+'@gbapakkau.cok'
    userIdForm = "4666932100"+str(i)
    password   = 'MMAKASIH SPAM BERHASIL '*10000+str(i)
    
    data = {
        'email'      : email,
        'password'   : password,
        'userIdForm' : userIdForm,
        'login'      : 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
