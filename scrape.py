import requests
from typing import List, Optional, Dict, Set
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from collections import deque
from parser import extract_main_content

BASE_URL: str = "https://www.notion.so/help/intro-to-databases"
RATE_LIMIT: int = 50

def get_webpage_content(url: str) -> Optional[str]:
  try:
    response = requests.get(url)
    response.raise_for_status()
    return response.text
  except requests.RequestException as e:
    print(f"An error occurred while fetching the webpage: {e}")
    return None

def get_webpage_links(content: str, base_url: str) -> List[str]:
  soup = BeautifulSoup(content, 'html.parser')
  links = set()
  for a_tag in soup.find_all('a', href=True):
    link = urljoin(base_url, a_tag['href'])
    # Remove fragment and query parameters
    parsed = urlparse(link)
    clean_link = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    links.add(clean_link)
  return sorted(links)

def is_relevant_link(link: str, base_url: str) -> bool:
  parsed_link = urlparse(link)
  parsed_base = urlparse(base_url)
  return (parsed_link.netloc == parsed_base.netloc and
          parsed_link.path.startswith('/help') and
          not parsed_link.path.startswith('/help/guides') and
          not parsed_link.path.startswith('/help/notion-academy'))

def scrape() -> Dict[str, str]:
  scraped_content: Dict[str, str] = {}
  to_visit: deque = deque([BASE_URL])
  to_visit_set: Set[str] = set([BASE_URL])
  
  while to_visit:
    current_url = to_visit.popleft()
    to_visit_set.remove(current_url)
    
    # don't visit already visited urls
    if current_url in scraped_content:
      continue
    
    content = get_webpage_content(current_url)

    if content:
      scraped_content[current_url] = extract_main_content(content)
      
      all_links = get_webpage_links(content, BASE_URL)
      new_relevant_links = [
        link for link in all_links 
        if is_relevant_link(link, BASE_URL) 
        and link not in scraped_content 
        and link not in to_visit_set
      ]
      
      for link in new_relevant_links:
        to_visit.append(link)
        to_visit_set.add(link)
      
      print(f"Scraped {current_url}")
    else:
      print(f"Failed to scrape: {current_url}")
  
  print(f"\nScraping complete. Total pages scraped: {len(scraped_content)}")

  return scraped_content