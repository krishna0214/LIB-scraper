#utils\extractUrlsfromText.py
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SUPPORTED_DOMAINS = {"www.iewc.com","www.tme.com"}  # Example supported domains, can be expanded

def extract_urls(file_content: str):
    """
    Extract URLs from the uploaded file content and categorize them as supported or unsupported.

    Args:
    - file_content (str): Raw content of the uploaded text file, containing comma-separated URLs.

    Returns:
    - tuple: (supported_urls, unsupported_urls)
      - supported_urls (list): List of URLs in supported domains.
      - unsupported_urls (list): List of URLs not in supported domains.
    """
    try:
        # Split and clean URLs
        urls = file_content.split(",")
        clean_urls = [url.strip() for url in urls if url.strip()]
        
        # Categorize URLs into supported and unsupported based on domain
        supported_urls = []
        unsupported_urls = []

        for url in clean_urls:
            domain = extract_domain(url)  # Helper function to extract domain
            #print(domain)
            logging.info(f"Processing URL: {url} | Domain: {domain}")
            if domain in SUPPORTED_DOMAINS:
                supported_urls.append(url)
            else:
                unsupported_urls.append(url)

        logging.info(f"Supported URLs: {supported_urls}")
        logging.info(f"Unsupported URLs: {unsupported_urls}")
        return supported_urls, unsupported_urls

    except Exception as e:
        logging.error(f"Error while extracting URLs: {str(e)}")
        raise e

def extract_domain(url: str):
    """
    Extract the domain name from a given URL.

    Args:
    - url (str): The URL string.

    Returns:
    - str: The domain name extracted from the URL.
    """
    try:
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        return parsed_url.netloc
    except Exception as e:
        logging.error(f"Failed to extract domain from URL '{url}': {str(e)}")
        return ""
