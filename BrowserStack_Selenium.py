import os
import time
import json
from collections import Counter
import browserstack_runner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from googletrans import Translator

BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

translator = Translator()
OPINION_SECTION = 'https://elpais.com/opinion/'

def setup_browserstack_driver(cap):
    cap['bstack:options'] = {
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
        "sessionName": cap.get("name", "Selenium Session"),
        "buildName": "Cross-Browser El Pais Scrape"
    }
    return webdriver.Remote(
        command_executor=f'https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=cap
    )

def run_scrape_on_browserstack(cap):
    driver = setup_browserstack_driver(cap)
    wait = WebDriverWait(driver, 10)
    data = []

    try:
        driver.get(OPINION_SECTION)
        time.sleep(2)
        print(f"✅ [{cap['name']}] Page loaded")

        articles = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article a'))
        )[:5]
        hrefs = [a.get_attribute('href') for a in articles if a.get_attribute('href')]

        for link in hrefs:
            driver.get(link)
            time.sleep(2)
            title = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1'))).text.strip()
            content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article'))).text.strip()
            data.append({'title': title, 'content': content})
            print(f"📰 {title}")

    except Exception as e:
        print(f"❌ [{cap['name']}] Failed: {e}")
    finally:
        driver.quit()

    # Translate and analyze
    translated = []
    for entry in data:
        try:
            tr = translator.translate(entry['title'], src='es', dest='en').text
            translated.append(tr)
        except:
            pass

    counter = Counter(word for title in translated for word in title.lower().split())
    print(f"\n[{cap['name']}] Repeated Words:")
    for word, freq in counter.items():
        if freq > 2:
            print(f"🔁 {word}: {freq}x")

# You can pass different capabilities into this function from another script/thread