# webscraper-and-chunker

Webscraper to scrape Notion help documentation

## Prerequisites

This project uses pyenv to manage Python versions. If you don't have pyenv installed, follow these steps:

### Installing pyenv on macOS:

```bash
brew update
brew install pyenv
```

After installation, add the following to your shell configuration file (.bashrc, .zshrc, etc.):

```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Restart your terminal to apply the changes.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Set up the Python environment:

   ```
   pyenv install
   ```

   This command will automatically install the correct version of python

3. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate
   ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Method

Scraping was pretty straightforward - chunking and group were definitely the harder parts of this project. I initially tried an approach using LangChain's
HTML splitters but found that the end generated chunks/content weren't super great (it often failed to detect specific headers and actually split the content by section). The end content generated also seemed to be a bit of a mess and not super well formatted.

For the final approach I found a library called html2text that did quite a good job of making the content readable and preserving the semantic presence of links, headers, and bullet lists, and I quite liked the end result. Thus I opted to prettify first (although I doubt this would be a good idea for a production
system, it worked quite well for a quick and dirty project like this), and then chunk afterwards. To chunk intelligently, I first split the entire string
by newline, and then calculated the neighboring cosine similarities of each chunk. I kept joining by similarity (the most similar chunks would be joined first)
until we could not join any further without going over 750 characters. The end result did quite a good job of keeping headers with paragraphs, and bulleted
lists together, and outputted human readable content nicely.

## Testing

Go into main.py and change the for loop on line 16 to index into whatever Notion help link you want to inspect the generated chunks.
