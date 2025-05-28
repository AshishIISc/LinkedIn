Here's the corrected `README.md` with your exact endpoints:

```markdown
# URL Scraper API with FastAPI

A web application that scrapes website content with both UI and API interfaces, deployed on Vercel.

## Features
- 🌐 Web UI for easy testing
- 🔌 REST API for programmatic access
- 📄 JSON responses/downloads
- 🔍 Extracts:
  - Page title
  - Meta description
  - Main text content

## Access Points

### Web Interface
```
https://linked-in-five-sigma.vercel.app/
```

### API Endpoint
```
GET https://linked-in-five-sigma.vercel.app/scrape
```

## API Usage

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | URL to scrape |
| `extract_text` | boolean | No | Whether to extract main text (default: true) |

### Example Requests

**Using cURL:**
```bash
# Basic request
curl "https://linked-in-five-sigma.vercel.app/scrape?url=https://example.com"

# Without text extraction
curl "https://linked-in-five-sigma.vercel.app/scrape?url=https://example.com&extract_text=false"

# Download as JSON file
curl "https://linked-in-five-sigma.vercel.app/scrape?url=https://example.com" -o result.json
```

**Using Python:**
```python
import requests

response = requests.get(
    "https://linked-in-five-sigma.vercel.app/scrape",
    params={
        "url": "https://example.com",
        "extract_text": True
    }
)
print(response.json())
```

### Response Format
```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "description": "This domain is for use in illustrative examples...",
  "text_content": "Example Domain\nThis domain...",
  "status": "success"
}
```

## Web Interface Instructions
1. Visit https://linked-in-five-sigma.vercel.app/
2. Enter URL in the input field
3. Toggle "Extract text content" if needed
4. View results or download as JSON

## Project Structure
```
.
├── main.py              # FastAPI application
├── vercel.json          # Vercel config
├── requirements.txt     # Dependencies
├── scraper.py           # Scraping logic
├── static/              # CSS files
└── templates/           # HTML templates
```
