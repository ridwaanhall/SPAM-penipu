import requests
import string
import random
from time import sleep

class PhishingSpammer:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        # self.delay = delay

    def generate_random_string(self, length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def generate_form_data(self):
        user = f"{self.generate_random_string(8)}@gmail.com"
        password = self.generate_random_string(15)
        form_data = {
            'user': user,
            'pass': password,
            'login': 'Facebook'
        }
        return form_data

    def send_request(self):
        form_data = self.generate_form_data()
        try:
            response = requests.post(self.url, data=form_data, headers=self.headers)
            print(f"Status Code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def start_spamming(self, count):
        for _ in range(count):
            self.send_request()
            # sleep(self.delay)

if __name__ == "__main__":
    url = "https://fkn4ik.aweys.net/proses/snd1.php"
    headers = {
        'authority': 'fkn4ik.aweys.net',
        'method': 'POST',
        'path': '/proses/snd1.php',
        'scheme': 'https',
        'accept': 'text/plain, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9,mt;q=0.8',
        'content-length': '66',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://fkn4ik.aweys.net',
        'priority': 'u=1, i',
        'referer': 'https://fkn4ik.aweys.net/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    spammer = PhishingSpammer(url, headers)
    spammer.start_spamming(11111111111111111111)
