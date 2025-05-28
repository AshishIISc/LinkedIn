import httpx
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re


async def scrape_url(url: str, extract_text: bool = True) -> Dict[str, Optional[str]]:
    """
    Scrape a URL and return its title, description, and main text content.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, follow_redirects=True, timeout=10.0)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise Exception(f"HTTP error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching URL: {str(e)}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title = soup.title.string if soup.title else None

        # Extract description
        description = None
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            description = meta_desc.get('content')

        # Extract main text content
        text_content = None
        if extract_text:
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = '\n'.join(chunk for chunk in chunks if chunk)
            text_content = re.sub(r'\n\s*\n', '\n\n', text_content)

        return {
            "title": title,
            "description": description,
            "text_content": text_content
        }
