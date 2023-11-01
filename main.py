from bs4 import BeautifulSoup, Comment, Tag
from utils import fetch_url_content, map_roles_to_tags, strip_unnecessary_attributes, flatten_structure
import requests

def reduce_dom(html_content):
    """
    Dimensionally reduce the HTML DOM.
    
    Parameters:
    - html_content (str): Raw HTML content to be reduced.
    
    Returns:
    - BeautifulSoup object: The reduced DOM.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove all <style> tags
    for style in soup.find_all('style'):
        style.decompose()
    
    # Remove inline styles
    for tag in soup.find_all(style=True):
        del tag['style']

    # Remove all <script> tags
    for script in soup.find_all('script'):
        script.decompose()
    
    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Remove all <link> tags
    for link_tag in soup.find_all('link'):
        link_tag.decompose()

    # Remove all <meta> tags
    for meta_tag in soup.find_all('meta'):
        meta_tag.decompose()


    soup = map_roles_to_tags(soup)
    soup = strip_unnecessary_attributes(soup) 
    soup = flatten_structure(soup)
    return soup




if __name__ == "__main__":
    content = fetch_url_content("https://github.com/kaavee315")
    # content = """<div><span><p>Some text here.</p></span></div>"""
    if content:
        reduced_soup = reduce_dom(content)
        print(reduced_soup.prettify())


