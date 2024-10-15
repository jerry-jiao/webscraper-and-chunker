from chunker import chunk
from formatter import convert_to_readable
from scrape import scrape

def main() -> None:
  webpage_htmls = scrape()
  content = {}

  for k in webpage_htmls.keys():
    content[k] = chunk(convert_to_readable(webpage_htmls[k]))

  for i, content_chunk in enumerate(content["https://www.notion.so/help/enterprise-admins"]):
    print('Chunk {} | {} characters\n'.format(i, len(content_chunk)), content_chunk)

if __name__ == "__main__":
  main()