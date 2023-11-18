import requests

url = 'https://293.p5c2b.com/data.php'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

loop_value = int(input("bar bar brp kali? : "))

for i in range(1, loop_value+1):
    email = str(i) +'''
    ⚠️ السارق و السارقة فاقطعوا أيديهما|
    Artinya: "Pelaku pencurian laki-laki dan perempuan, potonglah kedua tangannya."
    (HR. Al-Bukhari dan Muslim) ⚠️
    |
    ⚠️ Pasal 30-32 Ayat (1) UU ITE|
    pidana penjara paling lama 6 tahun dan/atau denda paling banyak 1 miliar rupiah. ⚠️
    BY : -FRNDS🖕🖕🖕'''*10000
    
    data = {
        'playid'    : '666666666',
        'level'     : '19',
        'tier'      : 'Mythic Glory',
        'elitepass' : 'Pernah',
        'email'     : email,
        'password'  : 'Masih zaman tipu2 dek-dek, mo beli Rubicon kah?🗿',
        'login'     : 'Facebook'
    }
    
    response = requests.post(url, data=data, headers=headers)
    print("bang udah bang", i)
