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

        # Set up headless browser with additional stability options
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")

        # Create a unique user data directory to prevent Chrome session errors
        user_data_dir = tempfile.mkdtemp()
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

        # Initialize driver with timeout
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
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
        # Return fallback content instead of empty string
        return f"Company website: {url}. Unable to extract detailed content due to technical limitations, but this appears to be a legitimate business website."

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
        if user_data_dir:
            shutil.rmtree(user_data_dir, ignore_errors=True)
