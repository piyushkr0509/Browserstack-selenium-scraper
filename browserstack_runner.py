import time
import threading
from BrowserStack_Selenium import run_scrape_on_browserstack  # Import scraper function

if __name__ == "__main__":
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

    # **Run tests concurrently on all devices**
    threads = []
    for cap in BROWSER_CONFIGS:
        t = threading.Thread(target=run_scrape_on_browserstack, args=(cap,))
        t.start()
        threads.append(t)
        time.sleep(1)  # Small delay to avoid overwhelming BrowserStack

    # **Ensure all threads finish execution**
    for t in threads:
        t.join()

    print("\n✅ All cross-browser scraping tests completed.")
