import requests
import string
import random
from time import sleep
from tqdm import tqdm

class PhishingSpammer:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def generate_random_string(self, length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def generate_form_data(self):
        user = f"{self.generate_random_string(8)}@gmail.com"
        password = self.generate_random_string(15)
        form_data = {
            'email': user,
            'sandi': password,
            'login': 'Facebook'
        }
        return form_data

    def send_request(self):
        form_data = self.generate_form_data()
        try:
            response = requests.post(self.url, data=form_data, headers=self.headers)
            # if response.status_code == 200:
            #     # print(f"Success: {form_data['email']} -> {form_data['sandi']}")
            # else:
            #     print(f"Failed with status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def start_spamming(self, count):
        for _ in tqdm(range(count), desc="Processing Requests"):
            self.send_request()
            # sleep(1)  # To avoid overloading the server, add a delay if needed

if __name__ == "__main__":
    url = "https://asd16.bvvka3.my.id/data.php"
    headers = {
        'accept': 'text/plain, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://asd16.bvvka3.my.id',
        'referer': 'https://asd16.bvvka3.my.id/index.php?gToken=verified/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    # Set a reasonable count value for spamming, e.g., 100
    spammer = PhishingSpammer(url, headers)
    spammer.start_spamming(99999999)  # Adjust count to a reasonable integer
