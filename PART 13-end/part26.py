import requests

url = 'https://urnbns7.ggkyyr1.biz.id/data.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = str(i) +'''
    | MAMPUS KONTOL MEMEK KAU ANJENG BABI BANGSAT NGENTOD ASU BAJINGAN | 
    your data KTP, KK, Location, Phone Number, IP has been hacked.
    '''*10000

    data = {
        'playid'    : '1010929381',
        'level'     : '100',
        'tier'      : 'Master',
        'elitepass' : 'Pernah',
        'email'     : email,
        'password'  : 'Masih zaman tipu2 dek-dek, mo beli Rubicon kah?🗿',
        'login'     : 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
