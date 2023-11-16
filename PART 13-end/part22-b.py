import requests

url = 'https://jajsjsjs.huftjs.art/free-fire/success.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    useridForm = "666932100"+str(i)
    
    data = {
        'useridForm' : useridForm,
        'nickname'   : 'player 43665570006'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
