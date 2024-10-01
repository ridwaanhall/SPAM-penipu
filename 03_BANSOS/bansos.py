import requests
import random
from tqdm import tqdm

class WebsiteTester:
    def __init__(self, phone_url, otp_url):
        self.phone_url = phone_url
        self.otp_url = otp_url

    def generate_random_number_suffix(self):
        # Generate a 10-digit random number as a string
        return ''.join([str(random.randint(0, 9)) for _ in range(10)])

    def generate_phone_number(self, random_suffix):
        # Create phone number starting with '08' and append the random suffix
        return '08' + random_suffix
    
    def generate_full_number(self, random_suffix):
        # Create full number starting with '+62' and append the same random suffix
        return '+62' + random_suffix

    def generate_random_otp(self):
        # Generate a random 5-digit OTP
        return ''.join([str(random.randint(0, 9)) for _ in range(5)])

    def send_phone_number(self):
        random_suffix = self.generate_random_number_suffix()
        phone_number = self.generate_phone_number(random_suffix)
        full_number = self.generate_full_number(random_suffix)

        payload = {
            'phoneNumber': phone_number,
            'full_number': full_number
        }
        response = requests.post(self.phone_url, data=payload)
        return response.status_code

    def send_otp(self):
        otp = self.generate_random_otp()
        payload = {
            'phone': '',  # Can be adjusted if needed
            'otpku': otp
        }
        response = requests.post(self.otp_url, data=payload)
        return response.status_code

# Usage
if __name__ == "__main__":
    phone_url = "https://info-bantuan-bansos-pkh.jukiop.us/m/xcode.php"
    otp_url = "https://info-bantuan-bansos-pkh.jukiop.us/m/auth/two.php"

    tester = WebsiteTester(phone_url, otp_url)
    
    # Get the number of iterations from the user
    num_iterations = 100000

    # Use tqdm for progress bar
    for _ in tqdm(range(num_iterations)):
        # Send random phone number and full number with matching suffix
        tester.send_phone_number()
        
        # Send random OTP
        tester.send_otp()
