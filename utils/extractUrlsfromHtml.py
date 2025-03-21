#utils\extractUrlsfromHtml.py

from bs4 import BeautifulSoup
import json
from .extractUrlsfromText import SUPPORTED_DOMAINS
from distributorscripts.tme import fix_tme_urls
import re


def matches_search_criteria(url, search_list):
    """
    Check if the URL matches any item in the search list.
    
    Args:
        url (str): The URL to check.
        search_list (list): List of search terms.
        
    Returns:
        bool: True if the URL matches any search term, False otherwise.
    """
    if not search_list:
        return True  # If search_list is empty, consider all URLs as matching
    
    url_lower = url.lower()
    for term in search_list:
        if term.lower() in url_lower:
            return True
    return False

def extract_urls_from_html(raw_html, domain, search_list=None):
    """
    Extracts unique URLs from raw HTML content that match the search criteria.
    Args:
        raw_html (str): The raw HTML string.
        search_list (list, optional): List of search terms to filter URLs.
    Returns:
        list: A list of unique URLs extracted from the HTML that match the search criteria.
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    # Extract URLs from <a> tags with href attributes
    all_urls = [a['href'] for a in soup.find_all('a', href=True)]
    
    # Filter URLs based on search criteria
    #filtered_urls = [url for url in all_urls if matches_search_criteria(url, search_list)]
    if domain == "tme":
        all_urls= fix_tme_urls(all_urls)
    
    # Remove duplicates
    unique_urls = list(set(all_urls))
    
    return unique_urls







# Example usage:
# user_input = st.sidebar.text_input(
#     "Enter comma-separated items (e.g., glx,gxt):",
#     value="",
#     help="Enter items separated by commas, without spaces"
# )

# if user_input:
#     search_list = [item.strip() for item in user_input.split(',')]
# else:
#     search_list = []

# urls = extract_urls_from_html(raw_html, search_list)
