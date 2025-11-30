import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def search_web(query: str) -> str:
    """Searches the web for the given query and returns a summary of results.
    
    Args:
        query: The search query string.
        
    Returns:
        str: A formatted string containing titles, snippets, and URLs of the top results.
    """
    try:
        results = DDGS().text(keywords=query, max_results=5)
        if not results:
            return "No results found."
        
        formatted_results = "Search Results:\n"
        for i, r in enumerate(results, 1):
            formatted_results += f"{i}. {r['title']}\n   {r['body']}\n   URL: {r['href']}\n\n"
        return formatted_results
    except Exception as e:
        return f"Error performing search: {str(e)}"

def read_url(url: str) -> str:
    """Reads the content of a specific URL and returns the text.
    
    Args:
        url: The URL to read.
        
    Returns:
        str: The text content of the page, or an error message.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text()
        
        # Break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text[:5000] + "..." if len(text) > 5000 else text
    except Exception as e:
        return f"Error reading URL: {str(e)}"
