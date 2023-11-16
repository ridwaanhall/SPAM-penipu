import requests

url = 'https://co23.ndxy.my.id/data.php' #BTG6ZO
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = str(i) +'''
    | MARKOCOP KW ⚠️ kena sspam wkwkw ⚠️|
    ⚠️ bang udah bang ⚠️ | 
    CIE DATANYA DIHAPUS wkwkwk link baru
    |BY : -FRNDS 🖕🖕🖕'''*10000

    data = {
        'email' : email
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
