#api\api.py

import logging
from firecrawl import FirecrawlApp

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class FirecrawlAPI:
    def __init__(self, api_key: str):
        """
        Initialize the Firecrawl app with the provided API key.
        
        Args:
        - api_key (str): The API key for authentication with FirecrawlApp.
        """
        try:
            self.app = FirecrawlApp(api_key=api_key)
        except Exception as e:
            logging.error(f"Failed to initialize FirecrawlApp: {str(e)}")
            raise e  # Re-raise exception for critical issues

    def batch_process(self, urls: list, output_format: dict):
        """
        Scrape multiple URLs in batch.

        Args:
        - urls (list): A list of URLs to scrape.
        - output_format (dict): Specifies the format and rules for extracting data,
          e.g., {"format": "html", "wait_time": 5}.
        
        Returns:
        - dict: Scraped results from the specified URLs.
        
        Raises:
        - ValueError: If input arguments are invalid.
        - Exception: If batch scraping fails for any reason.
        """
        # Validate input arguments
        if not isinstance(urls, list) or not urls:
            logging.error("Invalid 'urls' argument. It must be a non-empty list.")
            raise ValueError("'urls' must be a non-empty list of URL strings.")
        if not isinstance(output_format, dict) or "formats" not in output_format:
            logging.error("Invalid 'output_format' argument. It must be a dictionary containing 'formats'.")
            raise ValueError("'output_format' must be a dictionary with required keys like 'formats'.")

        try:
            # Perform the batch scraping
            logging.info(f"Starting batch processing for {len(urls)} URLs...")
            results = self.app.batch_scrape_urls(urls, output_format)
            logging.info("Batch processing completed successfully.")
            return results
        except Exception as e:
            logging.error(f"Batch processing failed: {str(e)}")
            raise Exception("An error occurred during batch processing. Please check the logs.") from e

# # Usage Example
# if __name__ == "__main__":
#     try:
#         # Initialize API with your production key
#         api = FirecrawlAPI(api_key='fc-99d798a8d7b14941bdc5ffd1dXXX')

#         # Define URLs to scrape and the desired output format
#         urls_to_scrape = [
#             "https://example.com",
#             "https://example.org",
#         ]
#         output_preferences = {
#             "format": "rawHtml",  # Output format, e.g., HTML, JSON
#             "wait_time": 5000     # Time to wait for page loading in seconds
#         }

#         # Call batch_process method
#         scraped_data = api.batch_process(urls_to_scrape, output_preferences)
#         print(scraped_data)
#     except Exception as e:
#         logging.error(f"An error occurred in the main program: {str(e)}")
