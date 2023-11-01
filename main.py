from bs4 import BeautifulSoup
import requests

def fetch_url_content(url):
    """
    Fetch the content of a given URL.
    
    Parameters:
    - url (str): The URL to fetch.
    
    Returns:
    - str: The content of the URL, or None if the fetch was unsuccessful.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

# Example usage:
content = fetch_url_content("https://www.example.com/")
print(content)
