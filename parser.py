from bs4 import BeautifulSoup

# from inspecting the notion pages, we see that they use semantic tags like <main> and <aside> for their docs which is great for us.
# if we were to extend this scraping system to other websites, we'd have to do something more generalized and customizable
def extract_main_content(html_content):
  soup = BeautifulSoup(html_content, 'html.parser')
  
  main_content = soup.find('main')
  
  if main_content:
    # Remove any <aside> tags within the main content
    for aside in main_content.find_all('aside'):
        aside.decompose()
    
    # Return the string representation of the remaining content
    return str(main_content)
  
  raise Exception("No <main> tag found in the HTML content.")
    