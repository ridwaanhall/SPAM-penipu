import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import logging
from typing import Optional, Dict, Any


class BansosHTMLFetcher:
    """
    Object-oriented HTML fetcher for bansos website
    Handles HTTP requests, HTML parsing, and data extraction
    """
    
    def __init__(self, base_url: str = "https://cek-daftar10.bantuansosial.org/home/"):
        """
        Initialize the HTML fetcher
        
        Args:
            base_url (str): The base URL to fetch HTML from
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.html_content = None
        self.soup = None
        
        # Set up headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        Update request headers
        
        Args:
            headers (Dict[str, str]): Dictionary of headers to set
        """
        self.headers.update(headers)
    
    def fetch_html(self, url: Optional[str] = None, timeout: int = 10) -> bool:
        """
        Fetch HTML content from the specified URL
        
        Args:
            url (Optional[str]): URL to fetch, defaults to base_url
            timeout (int): Request timeout in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        target_url = url or self.base_url
        
        try:
            self.logger.info(f"Fetching HTML from: {target_url}")
            
            response = self.session.get(
                target_url,
                headers=self.headers,
                timeout=timeout,
                allow_redirects=True
            )
            
            response.raise_for_status()  # Raise an exception for bad status codes
            
            self.html_content = response.text
            self.soup = BeautifulSoup(self.html_content, 'html.parser')
            
            self.logger.info(f"Successfully fetched HTML content ({len(self.html_content)} characters)")
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching HTML: {e}")
            return False
    
    def get_html_content(self) -> Optional[str]:
        """
        Get the raw HTML content
        
        Returns:
            Optional[str]: HTML content or None if not fetched
        """
        return self.html_content
    
    def get_parsed_soup(self) -> Optional[BeautifulSoup]:
        """
        Get the parsed BeautifulSoup object
        
        Returns:
            Optional[BeautifulSoup]: Parsed soup object or None if not fetched
        """
        return self.soup
    
    def save_html_to_file(self, filename: str = "bansos_html.html") -> bool:
        """
        Save HTML content to a file
        
        Args:
            filename (str): Name of the file to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.html_content:
            self.logger.error("No HTML content to save. Fetch HTML first.")
            return False
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.html_content)
            
            self.logger.info(f"HTML content saved to: {filename}")
            return True
            
        except IOError as e:
            self.logger.error(f"Error saving HTML to file: {e}")
            return False
    
    def extract_forms(self) -> list:
        """
        Extract all forms from the HTML
        
        Returns:
            list: List of form elements
        """
        if not self.soup:
            self.logger.error("No parsed HTML available. Fetch HTML first.")
            return []
        
        forms = self.soup.find_all('form')
        self.logger.info(f"Found {len(forms)} forms in the HTML")
        return forms
    
    def extract_links(self) -> list:
        """
        Extract all links from the HTML
        
        Returns:
            list: List of link URLs
        """
        if not self.soup:
            self.logger.error("No parsed HTML available. Fetch HTML first.")
            return []
        
        links = []
        for link in self.soup.find_all('a', href=True):
            absolute_url = urljoin(self.base_url, link['href'])
            links.append({
                'text': link.get_text(strip=True),
                'url': absolute_url,
                'relative_url': link['href']
            })
        
        self.logger.info(f"Found {len(links)} links in the HTML")
        return links
    
    def extract_meta_info(self) -> Dict[str, Any]:
        """
        Extract meta information from the HTML
        
        Returns:
            Dict[str, Any]: Dictionary containing meta information
        """
        if not self.soup:
            self.logger.error("No parsed HTML available. Fetch HTML first.")
            return {}
        
        meta_info = {}
        
        # Extract title
        title = self.soup.find('title')
        meta_info['title'] = title.get_text(strip=True) if title else None
        
        # Extract meta tags
        meta_tags = {}
        for meta in self.soup.find_all('meta'):
            if meta.get('name'):
                meta_tags[meta.get('name')] = meta.get('content')
            elif meta.get('property'):
                meta_tags[meta.get('property')] = meta.get('content')
        
        meta_info['meta_tags'] = meta_tags
        
        self.logger.info("Extracted meta information from HTML")
        return meta_info
    
    def search_text(self, search_term: str) -> list:
        """
        Search for specific text in the HTML content
        
        Args:
            search_term (str): Text to search for
            
        Returns:
            list: List of elements containing the search term
        """
        if not self.soup:
            self.logger.error("No parsed HTML available. Fetch HTML first.")
            return []
        
        results = self.soup.find_all(text=lambda text: text and search_term.lower() in text.lower())
        self.logger.info(f"Found {len(results)} occurrences of '{search_term}'")
        return results
    
    def get_page_stats(self) -> Dict[str, int]:
        """
        Get basic statistics about the HTML page
        
        Returns:
            Dict[str, int]: Dictionary with page statistics
        """
        if not self.soup:
            self.logger.error("No parsed HTML available. Fetch HTML first.")
            return {}
        
        stats = {
            'total_elements': len(self.soup.find_all()),
            'forms': len(self.soup.find_all('form')),
            'links': len(self.soup.find_all('a')),
            'images': len(self.soup.find_all('img')),
            'scripts': len(self.soup.find_all('script')),
            'stylesheets': len(self.soup.find_all('link', rel='stylesheet')),
            'divs': len(self.soup.find_all('div')),
            'inputs': len(self.soup.find_all('input')),
        }
        
        return stats
    
    def close_session(self) -> None:
        """Close the requests session"""
        self.session.close()
        self.logger.info("Session closed")


def main():
    """
    Main function to demonstrate the HTML fetcher usage
    """
    # Create an instance of the HTML fetcher
    fetcher = BansosHTMLFetcher()
    
    # Fetch HTML content
    if fetcher.fetch_html():
        print("HTML content fetched successfully!")
        
        # Get raw HTML
        html = fetcher.get_html_content()
        print(f"HTML length: {len(html)} characters")
        
        # Save HTML to file
        fetcher.save_html_to_file("bansos_page.html")
        
        # Extract page information
        meta_info = fetcher.extract_meta_info()
        print(f"Page title: {meta_info.get('title', 'No title')}")
        
        # Get page statistics
        stats = fetcher.get_page_stats()
        print("\nPage Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Extract forms
        forms = fetcher.extract_forms()
        print(f"\nFound {len(forms)} forms on the page")
        
        # Extract links
        links = fetcher.extract_links()
        print(f"Found {len(links)} links on the page")
        
        # Print first few links as example
        if links:
            print("\nFirst few links:")
            for i, link in enumerate(links[:5]):
                print(f"  {i+1}. {link['text']} -> {link['url']}")
        
        # Search for specific text
        bansos_mentions = fetcher.search_text("bansos")
        print(f"\nFound {len(bansos_mentions)} mentions of 'bansos'")
        
    else:
        print("Failed to fetch HTML content")
    
    # Close the session
    fetcher.close_session()


if __name__ == "__main__":
    main()