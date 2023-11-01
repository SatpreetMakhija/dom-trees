import requests
from bs4 import BeautifulSoup, Tag

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
        # This will raise an HTTPError if the HTTP request
        # returned an unsuccessful status code.
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None


def map_roles_to_tags(soup):
    """
    Maps ARIA roles to custom tag names. It's purpose is to standardise HTML DOM across websites.
    For example, a website could use a <div> tag as a button but having an onClick function attached to it.
    Therefore, we rename the div tab to a btn.

    Args:
    - soup (BeautifulSoup): The parsed BeautifulSoup object
    
    Returns:
    - BeautifulSoup: The modified soup object with tags renamed based on roles
    """
    
    role_to_tag_mapping = {
        'button': 'btn',
        'navigation': 'nav',
        'complementary': 'complementary',
        'contentinfo': 'info',
        'main': 'primary-content',
        'search': 'search-box',
        'form': 'input-sect',
        'article': 'content-unit',
        'alert': 'alert-box',
        'dialog': 'popup-box',
        'listbox': 'list-container',
        'menu': 'menu-list',
        'progressbar': 'progress-ind',
        'tooltip': 'hint-box',
        'tab': 'nav-tab',
        'presentation': 'display-item',
        'link': 'nav-link'
    }

    for element in soup.find_all(True):  # Iterates over all tags in the soup
        role = element.get('role')
        if role in role_to_tag_mapping:
            element.name = role_to_tag_mapping[role]

    return soup



def strip_unnecessary_attributes(soup):
    """Remove attributes that may not be relevant for user intent."""
    # List of attributes to remove
    attrs_to_remove = ["class", "style", "id", "lang", "srcset", "sizes", "rel"]
    
    for tag in soup.find_all(True):  # Iterate over all tags
        for attr in attrs_to_remove:
            if attr in tag.attrs:  # Check if attribute exists
                del tag.attrs[attr]  # Remove the attribute

        # Remove data-* attributes
        data_attrs = [attr for attr in tag.attrs.keys() if attr.startswith('data-')]
        for attr in data_attrs:
            del tag.attrs[attr]
    
    return soup



def flatten_structure(soup):
    """Flatten deeply nested structures where a tag contains only another tag."""
    # We first recursively flatten the children
    if isinstance(soup, Tag):
        for child in soup.children:
            flatten_structure(child)
        
        # If the current tag only contains a single tag, we unwrap it.
        if len(soup.contents) == 1 and isinstance(soup.contents[0], Tag):
            soup.contents[0].unwrap()

    return soup
    # # A flag to determine if any changes were made during a loop iteration
    # changes_made = True
    
    # while changes_made:  # Continue until no further flattening can be done
    #     changes_made = False
        
    #     # Iterate over all tags in the soup
    #     for tag in soup.find_all(True):
            
    #         # Check if the tag has only one child that's also a tag
    #         if len(tag.contents) == 1 and isinstance(tag.contents[0], Tag):
    #             tag.replace_with(tag.contents[0])
    #             changes_made = True

    # return soup
