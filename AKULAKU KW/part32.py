import requests
import random

url = 'https://m-akulaku1.my.id/OTP/0dataSMS.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
loop_value = int(input("jumlah spam : "))

for i in range(1, loop_value+1):
    start_nodeb = 4219313719837212
    end_nodeb = 9999999999999999
    random_number_deb = random.randint(start_nodeb, end_nodeb)
    random_nodeb = '{:04} {:04} {:04} {:04}'.format(
        random_number_deb // 10**12 % 10**4,
        random_number_deb // 10**8 % 10**4,
        random_number_deb // 10**4 % 10**4,
        random_number_deb % 10**4
    )
    aa = str(random.randint(1, 12)).zfill(2)
    bb = str(random.randint(23, 99))
    random_mb = f"{aa}/{bb}"
    
    random_number_cvv = random.randint(1, 99999)
    random_cvv = '{:05}'.format(random_number_cvv)
    
    data = {
        'sms': random_cvv
    }
    response = requests.post(url, data=data, headers=headers)
    #print("Successfully! with random : " + random_nodeb+ " | "+ random_mb+ " | "+ random_cvv)
    
    if response.status_code == 200:
        print("Successfully!! with random SMS : " + random_cvv)
    else:
        print("Error: Unexpected response code " + str(response.status_code))

