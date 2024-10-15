import html2text


def convert_to_readable(content):
  # Create an html2text converter
  converter = html2text.HTML2Text()
  # Configure the converter
  converter.ignore_links = False
  converter.body_width = 0  # No line wrapping
  
  # Convert HTML to Markdown-like text
  readable_text = converter.handle(content)
  
  return readable_text.strip()