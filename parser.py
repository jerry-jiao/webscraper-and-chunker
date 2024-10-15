from bs4 import BeautifulSoup

def extract_main_content(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the <main> tag
    main_content = soup.find('main')
    
    if main_content:
        # Remove any <aside> tags within the main content
        for aside in main_content.find_all('aside'):
            aside.decompose()
        
        # Return the string representation of the remaining content
        return str(main_content)
    else:
        return "No <main> tag found in the HTML content."
    