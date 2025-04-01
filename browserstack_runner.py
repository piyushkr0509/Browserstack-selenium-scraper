import os
import json
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
OPINION_SECTION = "https://elpais.com/opinion/"
# Test configurations
BROWSER_CONFIGS = [
    {
        'os': 'Windows',
        'os_version': '10',
        'browser': 'Chrome',
        'browser_version': 'latest',
        'name': 'Chrome_Windows'
    },
    {
        'os': 'OS X',
        'os_version': 'Sonoma',
        'browser': 'Safari',
        'browser_version': 'latest',
        'name': 'Safari_macOS'
    },
    {
        'os': 'Windows',
        'os_version': '11',
        'browser': 'Firefox',
        'browser_version': 'latest',
        'name': 'Firefox_Windows'
    },
    {
        'device': 'Samsung Galaxy S23',
        'real_mobile': 'true',
        'os_version': '13.0',
        'browserName': 'Chrome',
        'name': 'Chrome_Android'
    },
    {
        'device': 'iPhone 15',
        'real_mobile': 'true',
        'os_version': '17',
        'browserName': 'Safari',
        'name': 'Safari_iPhone'
    }
]
def run_test(cap):
    capabilities = {
        'bstack:options': {
            'userName': BROWSERSTACK_USERNAME,
            'accessKey': BROWSERSTACK_ACCESS_KEY,
            'sessionName': cap.get('name', 'Selenium Session'),
        }
    }
    # Merge browser/device capabilities
    capabilities.update(cap)
    url = f'https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub'
    # Create an instance of Options
    options = webdriver.ChromeOptions()
    options.set_capability('bstack:options', capabilities['bstack:options'])
    # Use the options argument instead of desired_capabilities
    driver = webdriver.Remote(command_executor=url, options=options)
    try:
        driver.get(OPINION_SECTION)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article a'))
        )
        print(f":white_check_mark: {cap['name']} - Page loaded successfully")
    except Exception as e:
        print(f":x: {cap['name']} - Test failed: {e}")
    finally:
        driver.quit()
# Launch 5 threads
threads = []
for cap in BROWSER_CONFIGS:
    t = threading.Thread(target=run_test, args=(cap,))
    t.start()
    threads.append(t)
for t in threads:
    t.join()
print(":white_check_mark: All cross-browser tests completed.")
