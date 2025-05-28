from fastapi import FastAPI, HTTPException, Query, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from scraper import scrape_url
import logging
import json

app = FastAPI(
    title="URL Scraper API",
    description="API for scraping website content with UI",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScrapeResult(BaseModel):
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    text_content: Optional[str] = None
    status: str
    error: Optional[str] = None


@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/scrape-ui", response_class=HTMLResponse, tags=["UI"])
async def scrape_via_ui(
    request: Request,
    url: str = Form(...),
    extract_text: bool = Form(True)
):
    try:
        result = await scrape_url(url, extract_text)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": {
                    "url": url,
                    "title": result.get("title"),
                    "description": result.get("description"),
                    "text_content": result.get("text_content") if extract_text else None,
                    "status": "success"
                },
                "json_data": json.dumps({
                    "url": url,
                    "title": result.get("title"),
                    "description": result.get("description"),
                    "text_content": result.get("text_content") if extract_text else None,
                    "status": "success"
                }, indent=2)
            }
        )
    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": str(e)
            }
        )


@app.get("/scrape", response_model=ScrapeResult, tags=["API"])
async def scrape_api(
    url: str = Query(..., description="URL to scrape"),
    extract_text: bool = Query(True, description="Whether to extract main text content")
):
    """
    Scrape a given URL and return its title, description, and main text content.
    """
    try:
        result = await scrape_url(url, extract_text)
        return {
            "url": url,
            "title": result.get("title"),
            "description": result.get("description"),
            "text_content": result.get("text_content") if extract_text else None,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "url": url,
                "status": "error",
                "error": str(e)
            }
        )


@app.get("/download-json", tags=["UI"])
async def download_json(
    url: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    text_content: Optional[str] = None
):
    data = {
        "url": url,
        "title": title,
        "description": description,
        "text_content": text_content
    }
    json_str = json.dumps(data, indent=2)
    return Response(
        content=json_str,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=scraped_data_{url.replace('/', '_')}.json"}
    )
