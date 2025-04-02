import os
import time
import json
import threading
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from googletrans import Translator

# BrowserStack Credentials
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

translator = Translator()
OPINION_SECTION = 'https://elpais.com/opinion/?locale=es' #Ensuring locale is spanish


# Common stopwords (to improve word frequency analysis)
STOPWORDS = {"the", "of", "and", "to", "in", "for", "on", "with", "at", "by", "from", "a", "an", "this", "that", "is"}

def setup_browserstack_driver(cap):
    cap['bstack:options'] = {
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
        "sessionName": cap.get("name", "Selenium Session"),
        "buildName": "Cross-Browser El Pais Scrape"
    }

    # For mobile devices, use 'browserName' instead of 'browser'
    if 'device' in cap:
        options = webdriver.ChromeOptions() if cap['browserName'] == 'Chrome' else webdriver.SafariOptions()
    else:
        options = webdriver.ChromeOptions()
    
    options.set_capability('bstack:options', cap['bstack:options'])
    return webdriver.Remote(
        command_executor=f'https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub',
        options=options
    )


def run_scrape_on_browserstack(cap):
    """Scrapes articles from El País and analyzes repeated words."""
    driver = setup_browserstack_driver(cap)
    wait = WebDriverWait(driver, 10)
    data = []

    try:
        driver.get(OPINION_SECTION)
        time.sleep(2)
        print(f"✅ [{cap['name']}] Page loaded")

        articles = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article a'))
        )[:5]  # Limit to 5 articles

        hrefs = [a.get_attribute('href') for a in articles if a.get_attribute('href')]

        for link in hrefs:
            driver.get(link)
            time.sleep(2)

            # Extract title & content
            title = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1'))).text.strip()
            content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article'))).text.strip()

            data.append({'title': title, 'content': content})
            print(f"📰 [{cap['name']}] {title}")

    except Exception as e:
        print(f"❌ [{cap['name']}] Failed: {e}")
    
    finally:
        driver.quit()

    # **Batch Translation for Efficiency**
    translated_titles = []
    try:
        translations = translator.translate([entry['title'] for entry in data], src='es', dest='en')
        translated_titles = [t.text for t in translations]
    except Exception as e:
        print(f"⚠️ [{cap['name']}] Translation failed: {e}")

    # **Word Frequency Analysis**
    word_counter = Counter(
        word.lower() for title in translated_titles for word in title.split() if word.lower() not in STOPWORDS
    )

    print(f"\n📊 [{cap['name']}] Repeated Words:")
    for word, freq in word_counter.most_common(5):  # Top 5 repeated words
        print(f"🔁 {word}: {freq}x")

    return data  # Return scraped data if needed

# Example Usage (if running standalone)
if __name__ == "__main__":
    test_capability = {
        'os': 'Windows',
        'os_version': '10',
        'browser': 'Chrome',
        'browser_version': 'latest',
        'name': 'Chrome_Windows'
    }
    run_scrape_on_browserstack(test_capability)
