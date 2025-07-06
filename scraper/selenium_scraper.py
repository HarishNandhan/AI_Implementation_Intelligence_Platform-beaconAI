import logging
import time
import tempfile
import shutil
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)

def scrape_company_website(url: str) -> str:
    """
    Uses Selenium to scrape JS-rendered company websites and extract clean text.
    
    Args:
        url (str): The URL of the company website or About page.

    Returns:
        str: Extracted readable text content from the page.
    """

    driver = None
    user_data_dir = None

    try:
        logger.info(f"[SCRAPER] Scraping: {url}")

        # Set up headless browser
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Create a unique user data directory to prevent Chrome session errors
        user_data_dir = tempfile.mkdtemp()
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(4)  # Wait for JS content to load

        # Parse content with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Remove noise (JS, CSS, Nav, etc.)
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n").strip()
        text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])

        logger.info(f"[SCRAPER] Extracted {len(text)} characters.")
        return text

    except Exception as e:
        logger.error(f"[SCRAPER ERROR] Failed to scrape {url}: {e}")
        return ""

    finally:
        if driver:
            driver.quit()
        if user_data_dir:
            shutil.rmtree(user_data_dir, ignore_errors=True)
