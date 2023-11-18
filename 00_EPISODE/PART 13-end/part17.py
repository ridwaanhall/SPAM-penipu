import requests

url = 'https://mso.qobx.my.id/data.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = str(i) +'''
    |⚠️ kena sspam wkwkkw ⚠️|⚠️ bang udah bang ⚠️
    lag bang lag|BY : -FRNDS 🖕🖕🖕'''*10000

    data = {
        'email'     : email,
        'sandi'  : 'Masih zaman tipu2 dek-dek, mo beli Rubicon kah?🗿',
        'login'     : 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
