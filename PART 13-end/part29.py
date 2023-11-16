import requests

url = input("Enter the URL : ")
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    message_to_hell = str(i) +'''
    . makasih bang gw dapet akun gratis, tinggal pilih2 woakwaokwaowa.
    nipu2 ga guna, kena spam iya kwoakwoakwoakwa.
    bang udah bang.
    otw ganti data.
    Don gk bang? donn.'''*10000

    data = {
        'playid'    : '1010929381',
        'level'     : '100',
        'tier'      : 'Master',
        'elitepass' : 'Pernah',
        'email'     : message_to_hell,
        'password'  : 'kdkaspdsapkp',
        'login'     : 'Facebook',
        #'phone'     : '12421321321321'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
