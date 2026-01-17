"""
Web scraping module for Bible commentaries from various sources
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import re
from urllib.parse import urljoin, urlparse
from config import USER_AGENT, REQUEST_TIMEOUT, MAX_RETRIES
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommentaryScraper:
    """Scraper for Bible commentaries from various sources"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def _make_request(self, url: str, retries: int = MAX_RETRIES) -> Optional[requests.Response]:
        """Make HTTP request with retries"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {retries} attempts")
        return None

    def _extract_text(self, soup: BeautifulSoup, selectors: List[str]) -> str:
        """Extract text using multiple CSS selectors"""
        text_parts = []
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text:
                    text_parts.append(text)
        return "\n\n".join(text_parts)

    def scrape_biblehub(self, book: str, chapter: int, verse: int) -> List[Dict]:
        """Scrape commentaries from BibleHub"""
        commentaries = []
        try:
            # BibleHub URL format
            book_lower = book.lower().replace(" ", "")
            url = f"https://biblehub.com/commentaries/{book_lower}/{chapter}-{verse}.htm"
            
            response = self._make_request(url)
            if not response:
                return commentaries

            soup = BeautifulSoup(response.content, "lxml")
            
            # Find commentary sections
            commentary_sections = soup.find_all("div", class_=re.compile("commentary|comment"))
            
            for section in commentary_sections:
                author_elem = section.find("h3") or section.find("h4")
                author = author_elem.get_text(strip=True) if author_elem else "Unknown"
                
                text_elem = section.find("p") or section
                text = text_elem.get_text(strip=True) if text_elem else ""
                
                if text:
                    commentaries.append({
                        "text": text,
                        "author": author,
                        "source": "BibleHub",
                        "url": url,
                        "source_type": "modern"
                    })
        except Exception as e:
            logger.error(f"Error scraping BibleHub for {book} {chapter}:{verse}: {e}")
        
        return commentaries

    def scrape_ccel(self, book: str, chapter: int, verse: int) -> List[Dict]:
        """Scrape commentaries from Christian Classics Ethereal Library"""
        commentaries = []
        try:
            # CCEL has various commentary formats
            # This is a template - actual implementation would need to adapt to their structure
            base_url = "https://www.ccel.org"
            # Search for commentaries
            search_url = f"{base_url}/search?q={book}+{chapter}+{verse}"
            
            response = self._make_request(search_url)
            if not response:
                return commentaries

            soup = BeautifulSoup(response.content, "lxml")
            
            # Extract commentary links and content
            links = soup.find_all("a", href=re.compile("commentary|father"))
            
            for link in links[:5]:  # Limit to first 5 results
                href = link.get("href")
                if href:
                    full_url = urljoin(base_url, href)
                    content_response = self._make_request(full_url)
                    
                    if content_response:
                        content_soup = BeautifulSoup(content_response.content, "lxml")
                        text = self._extract_text(content_soup, ["p", "div.content", "div.text"])
                        
                        if text and len(text) > 50:  # Minimum length check
                            author = link.get_text(strip=True) or "CCEL Author"
                            commentaries.append({
                                "text": text,
                                "author": author,
                                "source": "CCEL",
                                "url": full_url,
                                "source_type": "church_fathers" if "father" in href.lower() else "middle_ages"
                            })
        except Exception as e:
            logger.error(f"Error scraping CCEL for {book} {chapter}:{verse}: {e}")
        
        return commentaries

    def scrape_sefaria(self, book: str, chapter: int, verse: int) -> List[Dict]:
        """Scrape Jewish commentaries from Sefaria"""
        commentaries = []
        try:
            # Sefaria API or web scraping
            # Map Bible book names to Hebrew names if needed
            book_mapping = {
                "Genesis": "Bereshit",
                "Exodus": "Shemot",
                # Add more mappings as needed
            }
            
            hebrew_book = book_mapping.get(book, book)
            url = f"https://www.sefaria.org/{hebrew_book}.{chapter}.{verse}"
            
            response = self._make_request(url)
            if not response:
                return commentaries

            soup = BeautifulSoup(response.content, "lxml")
            
            # Extract commentary sections
            commentary_divs = soup.find_all("div", class_=re.compile("commentary|rashi|rambam"))
            
            for div in commentary_divs:
                text = div.get_text(strip=True)
                if text and len(text) > 30:
                    author_elem = div.find_previous("h2") or div.find_previous("h3")
                    author = author_elem.get_text(strip=True) if author_elem else "Jewish Commentary"
                    
                    commentaries.append({
                        "text": text,
                        "author": author,
                        "source": "Sefaria",
                        "url": url,
                        "source_type": "jewish"
                    })
        except Exception as e:
            logger.error(f"Error scraping Sefaria for {book} {chapter}:{verse}: {e}")
        
        return commentaries

    def scrape_verse(self, book: str, chapter: int, verse: int, source_types: List[str] = None) -> List[Dict]:
        """Scrape commentaries for a specific verse from all configured sources"""
        if source_types is None:
            source_types = ["modern", "church_fathers", "middle_ages", "jewish"]
        
        all_commentaries = []
        
        # Scrape from different sources based on type
        if "modern" in source_types:
            all_commentaries.extend(self.scrape_biblehub(book, chapter, verse))
        
        if "church_fathers" in source_types or "middle_ages" in source_types:
            all_commentaries.extend(self.scrape_ccel(book, chapter, verse))
        
        if "jewish" in source_types:
            all_commentaries.extend(self.scrape_sefaria(book, chapter, verse))
        
        return all_commentaries

    def search_web(self, query: str, max_results: int = 10) -> List[Dict]:
        """Generic web search for commentaries (can be enhanced with search APIs)"""
        # This is a placeholder - in production, you'd use Google Custom Search API,
        # Bing Search API, or similar
        logger.info(f"Web search for: {query}")
        # For now, return empty - implement with actual search API
        return []
