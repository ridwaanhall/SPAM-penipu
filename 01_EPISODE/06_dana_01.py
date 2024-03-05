import requests
import random

class ScamSpammer:
    def __init__(self, headers, base_url):
        self.headers = headers
        # self.base_url = base_url
        self.url_num = base_url + '3678fd6893fb190b400d9d618c79cf92.php'
        self.url_pin = base_url + '2f68d4e0d386ee468cd061afc288d287.php'
        self.url_otp = base_url + '9dd9f94bf970e28cfd0d1bbdac2879ce.php'

    def generate_num(self):
        return '8' + str(random.randint(10, 99)) + '-' + str(random.randint(0000, 9999)) + '-' + str(random.randint(0000, 9999))

    def generate_pin(self):
        return [str(random.randint(0, 9)) for _ in range(6)]

    def generate_otp(self):
        return [str(random.randint(0, 9)) for _ in range(4)]

    def send_request(self, url, data):
        response = requests.post(url, data=data, headers=self.headers)
        # print(f'{response.status_code}')
        print(f'{response.status_code} | {data}')

    def spam(self, count):
        for i in range(1, count+1):
            nohp = self.generate_num()
            nohp_data = {'nohp': nohp}
            self.send_request(self.url_num, nohp_data)

            pin = self.generate_pin()
            pin_data = {'pin1': pin[0], 'pin2': pin[1], 'pin3': pin[2], 'pin4': pin[3], 'pin5': pin[4], 'pin6': pin[5]}
            self.send_request(self.url_pin, pin_data)

            otp = self.generate_otp()
            otp_data = {'otp1': otp[0], 'otp2': otp[1], 'otp3': otp[2], 'otp4': otp[3]}
            self.send_request(self.url_otp, otp_data)

            print(f'{i:05}. nohp: {nohp} | pin: {"".join(pin)} | otp: {"".join(otp)}\n')
            # print(f'{i:05}. pin: {"".join(pin)} | otp: {"".join(otp)}\n')

if __name__ == '__main__':
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    }
    base_url = 'https://nbvgvvfh.link-rhesmi.my.id/ast/req/'
    
    scam_spammer = ScamSpammer(headers, base_url)
    loop_value = int(input("SPAM count: "))
    scam_spammer.spam(loop_value)