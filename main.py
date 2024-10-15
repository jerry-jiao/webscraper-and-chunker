from chunker import chunk
from formatter import convert_to_readable
from scrape import scrape

def main():
  print('Scraping')
  webpage_htmls = scrape()
  content_chunks = {}

  print('Chunking')
  for k in webpage_htmls.keys():
    content_chunks[k] = chunk(convert_to_readable(webpage_htmls[k]))

  print('Chunking complete')

  for i, content_chunk in enumerate(content_chunks["https://www.notion.so/help/enterprise-admins"]):
    print('Chunk {} | {} characters\n'.format(i, len(content_chunk)), content_chunk)

if __name__ == "__main__":
  main()