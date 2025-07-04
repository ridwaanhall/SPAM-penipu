import asyncio
import aiohttp
import time
import os
import random
from typing import List, Dict, Optional
import logging
from dataclasses import dataclass
import threading
from datetime import datetime


@dataclass
class RequestResult:
    """Data class to store request results"""
    url: str
    status_code: Optional[int]
    response_time: float
    success: bool
    timestamp: str
    error_message: Optional[str] = None
    content_length: Optional[int] = None


class WebsiteLoadTester:
    """
    Object-oriented load tester for websites
    Handles multiple concurrent requests with configurable rate limiting
    """
    
    def __init__(self, 
                 base_url: str = "https://cek-daftar10.bantuansosial.org/home/",
                 requests_per_second: int = 1000,
                 max_concurrent: int = 100):
        """
        Initialize the load tester
        
        Args:
            base_url (str): The base URL to make requests to
            requests_per_second (int): Number of requests per second
            max_concurrent (int): Maximum concurrent requests
        """
        self.base_url = base_url
        self.requests_per_second = requests_per_second
        self.max_concurrent = max_concurrent
        
        # Calculate optimal concurrent connections based on RPS
        self.max_concurrent = min(max_concurrent, max(100, requests_per_second // 10))
        
        # Results storage
        self.results: List[RequestResult] = []
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = None
        
        # Threading
        self.stop_event = threading.Event()
        self.stats_lock = threading.Lock()
        
        # Load user agents from file
        self.user_agents = self.load_user_agents()
        
        # Generate pool of random IPs for rotation
        self.ip_pool = self.generate_ip_pool(500)  # Generate 500 random IPs
        
        # Base headers template (User-Agent will be randomized per request)
        self.base_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',  # Removed 'br' (brotli) to avoid decoding issues
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Configure logging
        logging.basicConfig(
            level=logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def load_user_agents(self) -> List[str]:
        """
        Load user agents from ua.txt file
        
        Returns:
            List[str]: List of user agent strings
        """
        try:
            ua_file_path = os.path.join(os.path.dirname(__file__), 'ua.txt')
            with open(ua_file_path, 'r', encoding='utf-8') as f:
                user_agents = [line.strip() for line in f if line.strip()]
            
            if user_agents:
                self.logger.info(f"Loaded {len(user_agents)} user agents from ua.txt")
                return user_agents
            else:
                self.logger.warning("No user agents found in ua.txt, using default")
                return [self.get_default_user_agent()]
        
        except FileNotFoundError:
            self.logger.warning("ua.txt not found, using default user agent")
            return [self.get_default_user_agent()]
        
        except Exception as e:
            self.logger.error(f"Error loading user agents: {e}")
            return [self.get_default_user_agent()]
    
    def get_default_user_agent(self) -> str:
        """
        Get default user agent as fallback
        
        Returns:
            str: Default user agent string
        """
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    def get_random_headers(self) -> Dict[str, str]:
        """
        Get headers with random user agent and IP
        
        Returns:
            Dict[str, str]: Headers with random user agent and IP forwarding
        """
        headers = self.base_headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        
        # Add random IP headers to simulate different clients
        random_ip = random.choice(self.ip_pool)
        headers['X-Forwarded-For'] = random_ip
        headers['X-Real-IP'] = random_ip
        headers['X-Originating-IP'] = random_ip
        headers['X-Remote-IP'] = random_ip
        headers['X-Client-IP'] = random_ip
        
        # Add some additional randomization for realism
        if random.random() < 0.3:  # 30% chance to add referer
            referers = [
                'https://www.google.com/',
                'https://www.bing.com/',
                'https://duckduckgo.com/',
                'https://search.yahoo.com/',
                'https://www.facebook.com/',
                'https://twitter.com/',
                'https://www.youtube.com/'
            ]
            headers['Referer'] = random.choice(referers)
        
        if random.random() < 0.2:  # 20% chance to add DNT header
            headers['DNT'] = '1'
        
        # Randomize some header values slightly
        if random.random() < 0.5:
            headers['Accept-Language'] = random.choice([
                'en-US,en;q=0.9',
                'en-GB,en;q=0.9',
                'en-US,en;q=0.8,es;q=0.6',
                'en-US,en;q=0.9,fr;q=0.8',
                'en-US,en;q=0.9,de;q=0.8'
            ])
        
        return headers
    
    def generate_ip_pool(self, count: int = 500) -> List[str]:
        """
        Generate a pool of random IP addresses
        
        Args:
            count (int): Number of IPs to generate
            
        Returns:
            List[str]: List of random IP addresses
        """
        ip_pool = []
        
        for _ in range(count):
            # Generate random IP addresses from common ranges
            # Avoid private IP ranges and use realistic public IP ranges
            
            ranges = [
                # Common public IP ranges
                (1, 126),      # Class A (excluding 10.x.x.x and 127.x.x.x)
                (128, 191),    # Class B (excluding 172.16-31.x.x)
                (192, 223)     # Class C (excluding 192.168.x.x)
            ]
            
            # Choose a random range
            range_choice = random.choice(ranges)
            first_octet = random.randint(range_choice[0], range_choice[1])
            
            # Avoid specific private/reserved ranges
            if first_octet == 10:  # Skip 10.x.x.x
                first_octet = random.randint(11, 126)
            elif first_octet == 127:  # Skip 127.x.x.x
                first_octet = random.randint(128, 191)
            elif first_octet == 172:  # Handle 172.x.x.x carefully
                second_octet = random.randint(0, 15) if random.random() < 0.5 else random.randint(32, 255)
            elif first_octet == 192:  # Handle 192.x.x.x carefully
                second_octet = random.randint(0, 167) if random.random() < 0.5 else random.randint(169, 255)
            else:
                second_octet = random.randint(1, 254)
            
            # Generate remaining octets
            if first_octet not in [172, 192]:
                second_octet = random.randint(1, 254)
            
            third_octet = random.randint(1, 254)
            fourth_octet = random.randint(1, 254)
            
            ip = f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}"
            ip_pool.append(ip)
        
        # Add some real popular public DNS and CDN IPs for more realism
        real_ips = [
            "8.8.8.8", "8.8.4.4",  # Google DNS
            "1.1.1.1", "1.0.0.1",  # Cloudflare
            "208.67.222.222", "208.67.220.220",  # OpenDNS
            "199.85.126.20", "199.85.127.20",  # Norton DNS
            "185.228.168.10", "185.228.169.11",  # CleanBrowsing
            "76.76.19.19", "76.223.100.101",  # Alternate DNS
        ]
        
        # Add some real IPs to make it more realistic
        ip_pool.extend(real_ips[:50])  # Add up to 50 real IPs
        
        # Shuffle the pool
        random.shuffle(ip_pool)
        
        self.logger.info(f"Generated {len(ip_pool)} random IP addresses for rotation")
        return ip_pool
    
    async def make_single_request(self, session: aiohttp.ClientSession, url: str) -> RequestResult:
        """
        Make a single HTTP request
        
        Args:
            session: aiohttp session
            url: URL to request
            
        Returns:
            RequestResult: Result of the request
        """
        start_time = time.time()
        
        # Get random headers for each request
        request_headers = self.get_random_headers()
        
        try:
            # Add per-request timeout and retry logic
            async with session.get(
                url, 
                headers=request_headers, 
                ssl=False,
                timeout=aiohttp.ClientTimeout(total=15, connect=10)  # Increased timeout
            ) as response:
                # Just read the response without storing content to save memory
                try:
                    content = await response.text()
                    content_length = len(content)
                except:
                    # If content reading fails, just get the length from headers
                    content_length = int(response.headers.get('content-length', 0))
                
                response_time = time.time() - start_time
                
                result = RequestResult(
                    url=url,
                    status_code=response.status,
                    response_time=response_time,
                    success=200 <= response.status < 400,
                    timestamp=datetime.now().isoformat(),
                    content_length=content_length
                )
                
                return result
                
        except asyncio.TimeoutError:
            response_time = time.time() - start_time
            result = RequestResult(
                url=url,
                status_code=None,
                response_time=response_time,
                success=False,
                timestamp=datetime.now().isoformat(),
                error_message="Request timeout"
            )
            return result
            
        except Exception as e:
            response_time = time.time() - start_time
            error_msg = str(e)
            
            # Simplify common errors for better readability
            if "Can not decode content-encoding: brotli" in error_msg:
                error_msg = "Brotli encoding not supported"
            elif "Connection timeout" in error_msg:
                error_msg = "Connection timeout"
            elif "Too many open files" in error_msg:
                error_msg = "Too many connections"
            
            result = RequestResult(
                url=url,
                status_code=None,
                response_time=response_time,
                success=False,
                timestamp=datetime.now().isoformat(),
                error_message=error_msg
            )
            return result
    
    async def run_load_test(self, duration: int):
        """
        Run load test for specified duration
        
        Args:
            duration: Duration in seconds to run the test
        """
        # Calculate total requests needed
        total_requests = self.requests_per_second * duration
        
        # Create connector with optimized settings for high-load testing
        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent * 2,  # Allow more connections
            limit_per_host=self.max_concurrent,
            ttl_dns_cache=300,
            use_dns_cache=True,
            keepalive_timeout=60,  # Longer keepalive
            enable_cleanup_closed=True,
            force_close=False,  # Reuse connections
            limit_simultaneous_connections=self.max_concurrent
        )
        
        # Longer timeout to handle high load
        timeout = aiohttp.ClientTimeout(total=20, connect=15)
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        ) as session:
            
            self.start_time = time.time()
            tasks = []
            requests_sent = 0
            batch_number = 0
            
            # Calculate delay between batches to achieve target RPS
            batch_size = min(50, self.max_concurrent // 4)  # Smaller batches for better control
            batch_delay = batch_size / self.requests_per_second
            
            while requests_sent < total_requests and not self.stop_event.is_set():
                # Check if we should stop based on duration
                elapsed = time.time() - self.start_time
                if elapsed >= duration:
                    break
                
                # Create batch of concurrent requests
                current_batch_size = min(batch_size, total_requests - requests_sent)
                batch_tasks = []
                
                for _ in range(current_batch_size):
                    if requests_sent >= total_requests:
                        break
                    
                    task = asyncio.create_task(
                        self.make_single_request(session, self.base_url)
                    )
                    batch_tasks.append(task)
                    requests_sent += 1
                
                tasks.extend(batch_tasks)
                batch_number += 1
                
                # Wait for batch delay to control RPS
                if batch_delay > 0.001:  # Only delay if meaningful
                    await asyncio.sleep(batch_delay)
                
                # Process completed tasks periodically to manage memory
                if len(tasks) >= 500 or batch_number % 20 == 0:
                    completed_tasks = [task for task in tasks if task.done()]
                    
                    for task in completed_tasks:
                        try:
                            result = await task
                            self.add_result(result)
                        except Exception as e:
                            self.logger.error(f"Task error: {e}")
                    
                    # Remove completed tasks from the list
                    tasks = [task for task in tasks if not task.done()]
            
            # Wait for remaining tasks
            if tasks:
                print(f"Waiting for {len(tasks)} remaining requests to complete...")
                
                # Wait in smaller batches to show progress
                while tasks:
                    batch_to_wait = tasks[:100]
                    tasks = tasks[100:]
                    
                    results = await asyncio.gather(*batch_to_wait, return_exceptions=True)
                    
                    for result in results:
                        if isinstance(result, RequestResult):
                            self.add_result(result)
                        elif isinstance(result, Exception):
                            # Handle exceptions from tasks
                            error_result = RequestResult(
                                url=self.base_url,
                                status_code=None,
                                response_time=0,
                                success=False,
                                timestamp=datetime.now().isoformat(),
                                error_message=str(result)
                            )
                            self.add_result(error_result)
                    
                    if tasks:
                        print(f"Still waiting for {len(tasks)} requests...")
    
    def add_result(self, result: RequestResult):
        """
        Add a request result and update statistics
        
        Args:
            result: RequestResult to add
        """
        with self.stats_lock:
            self.results.append(result)
            self.total_requests += 1
            
            if result.success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1
    
    def get_statistics(self) -> Dict:
        """
        Get request statistics
        
        Returns:
            Dict: Statistics about the requests
        """
        with self.stats_lock:
            if self.total_requests == 0:
                return {
                    'total_requests': 0,
                    'successful_requests': 0,
                    'failed_requests': 0,
                    'success_rate': 0.0,
                    'elapsed_time': 0.0,
                    'actual_rps': 0.0,
                    'avg_response_time_ms': 0.0,
                    'min_response_time_ms': 0.0,
                    'max_response_time_ms': 0.0
                }
            
            response_times = [r.response_time for r in self.results if r.response_time is not None]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            # Calculate elapsed time and actual RPS
            elapsed_time = time.time() - self.start_time if self.start_time else 0
            actual_rps = self.total_requests / elapsed_time if elapsed_time > 0 else 0
            
            return {
                'total_requests': self.total_requests,
                'successful_requests': self.successful_requests,
                'failed_requests': self.failed_requests,
                'success_rate': (self.successful_requests / self.total_requests) * 100,
                'elapsed_time': elapsed_time,
                'actual_rps': actual_rps,
                'avg_response_time_ms': avg_response_time * 1000,
                'min_response_time_ms': min(response_times) * 1000 if response_times else 0,
                'max_response_time_ms': max(response_times) * 1000 if response_times else 0
            }
    
    def print_real_time_stats(self):
        """
        Print real-time statistics to terminal
        """
        stats = self.get_statistics()
        
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print("                    WEBSITE LOAD TESTER - REAL-TIME STATS")
        print("=" * 80)
        print(f"Target URL: {self.base_url}")
        print(f"Target RPS: {self.requests_per_second:,}")
        print(f"Max Concurrent: {self.max_concurrent:,}")
        print(f"User Agents: {len(self.user_agents)} | IP Pool: {len(self.ip_pool)}")
        print("-" * 80)
        print(f"Elapsed Time:       {stats['elapsed_time']:.2f} seconds")
        print(f"Total Requests:     {stats['total_requests']:,}")
        print(f"Successful:         {stats['successful_requests']:,} ({stats['success_rate']:.2f}%)")
        print(f"Failed:             {stats['failed_requests']:,} ({100 - stats['success_rate']:.2f}%)")
        print(f"Actual RPS:         {stats['actual_rps']:.2f}")
        print(f"Avg Response Time:  {stats['avg_response_time_ms']:.2f} ms")
        print(f"Min Response Time:  {stats['min_response_time_ms']:.2f} ms")
        print(f"Max Response Time:  {stats['max_response_time_ms']:.2f} ms")
        
        if stats['total_requests'] > 0:
            print("-" * 80)
            print("STATUS CODE BREAKDOWN:")
            
            # Count status codes
            status_codes = {}
            recent_results = self.results[-1000:] if len(self.results) > 1000 else self.results
            
            for result in recent_results:
                status = result.status_code if result.status_code else 'Error'
                status_codes[status] = status_codes.get(status, 0) + 1
            
            for status, count in sorted(status_codes.items()):
                percentage = (count / len(recent_results)) * 100
                print(f"  Status {status}: {count:,} ({percentage:.1f}%)")
        else:
            print("-" * 80)
            print("Initializing requests... Please wait...")
        
        print("-" * 80)
        print("Press Ctrl+C to stop the test")
        print("=" * 80)
    
    def print_final_stats(self):
        """Print final statistics after test completion"""
        stats = self.get_statistics()
        
        print("\n" + "=" * 80)
        print("                         FINAL TEST RESULTS")
        print("=" * 80)
        print(f"Test Duration:      {stats['elapsed_time']:.2f} seconds")
        print(f"Total Requests:     {stats['total_requests']:,}")
        print(f"Successful:         {stats['successful_requests']:,} ({stats['success_rate']:.2f}%)")
        print(f"Failed:             {stats['failed_requests']:,} ({100 - stats['success_rate']:.2f}%)")
        print(f"Target RPS:         {self.requests_per_second:,}")
        print(f"Actual RPS:         {stats['actual_rps']:.2f}")
        print(f"Avg Response Time:  {stats['avg_response_time_ms']:.2f} ms")
        print(f"Min Response Time:  {stats['min_response_time_ms']:.2f} ms")
        print(f"Max Response Time:  {stats['max_response_time_ms']:.2f} ms")
        print(f"Anonymization:      {len(self.user_agents)} User Agents, {len(self.ip_pool)} IP Addresses")
        
        # Show error breakdown if any
        if stats['failed_requests'] > 0:
            print("-" * 80)
            print("ERROR BREAKDOWN:")
            error_types = {}
            failed_results = [r for r in self.results if not r.success]
            
            for result in failed_results:
                error = result.error_message or f"HTTP {result.status_code}"
                error_types[error] = error_types.get(error, 0) + 1
            
            for error, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {error}: {count:,} times")
        
        print("=" * 80)
    
    def stop_test(self):
        """Stop the load test"""
        self.stop_event.set()
    
    async def run_test_with_monitoring(self, duration: int):
        """
        Run test with real-time monitoring
        
        Args:
            duration: Test duration in seconds
        """
        # Start monitoring in background
        def monitor():
            time.sleep(1)  # Initial delay
            while not self.stop_event.is_set():
                try:
                    self.print_real_time_stats()
                    time.sleep(1)
                except:
                    break
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        
        # Run the actual test
        await self.run_load_test(duration)


def get_user_input():
    """
    Get user input for test parameters
    
    Returns:
        tuple: (requests_per_second, duration)
    """
    print("=" * 80)
    print("                    WEBSITE LOAD TESTER")
    print("=" * 80)
    print("Target URL: https://cek-daftar10.bantuansosial.org/home/")
    print("=" * 80)
    
    while True:
        try:
            rps = int(input("Requests per second: "))
            if rps <= 0:
                print("Please enter a positive number")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    while True:
        try:
            duration = int(input("Duration (seconds): "))
            if duration <= 0:
                print("Please enter a positive number")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    return rps, duration


def main():
    """
    Main function to run the load tester
    """
    print("=" * 80)
    print("                    WEBSITE LOAD TESTER")
    print("=" * 80)
    print("Initializing... Checking dependencies...")
    
    # Try to install brotli for better compression support
    try:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "brotli", "--quiet"], 
                            capture_output=True)
        print("✓ Brotli compression support available")
    except:
        print("! Brotli not available - using gzip/deflate only")
    
    try:
        # Get user input
        rps, duration = get_user_input()
        
        # Calculate optimal concurrent connections (more conservative for stability)
        max_concurrent = min(500, max(50, rps // 20))  # Reduced for stability
        
        # Create and configure load tester first
        tester = WebsiteLoadTester(
            requests_per_second=rps,
            max_concurrent=max_concurrent
        )
        
        print(f"\nStarting load test...")
        print(f"  RPS: {rps:,}")
        print(f"  Duration: {duration} seconds")
        print(f"  Max Concurrent: {max_concurrent}")
        print(f"  Total Requests: {rps * duration:,}")
        print(f"  User Agents: {len(tester.user_agents)} different UAs loaded")
        print(f"  Sample UAs: {tester.user_agents[0][:80]}...")
        print(f"  Random IPs: Enabled with proxy rotation")
        print(f"  Optimizations: Random User Agents, Random IPs, No Brotli, Extended Timeouts, Connection Reuse")
        print("\nStarting in 3 seconds...")
        
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        # Run test
        asyncio.run(tester.run_test_with_monitoring(duration))
        
        # Show final results
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        tester.print_final_stats()
        
    except KeyboardInterrupt:
        print("\n\nTest stopped by user.")
        if 'tester' in locals():
            tester.stop_test()
            time.sleep(1)
            tester.print_final_stats()
    
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
