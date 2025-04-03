# BrowserStack Selenium Scraper Assignment
This project demonstrates skills in
**web scraping**,
**API integration**,
**text processing**,
**cross-browser automation**
**Selenium framework**
**BrowserStack**
---
## :pushpin: Assignment Goals
- Scrape the first 5 articles from the *Opinion* section of [El País](https://elpais.com/opinion/)
- Extract **titles**, **content**, and optionally **cover images**
- Translate Spanish titles to English using **Google Translate API**
- Analyze translated titles for **repeated words**
- Validate functionality across **5 parallel browser/device combinations** on **BrowserStack**
---
## :test_tube: Technologies Used
- Python 3.10+
- Selenium WebDriver
- Google Translate (via `googletrans`)
- BrowserStack Automate
- Multi-threading for parallel test runs
---
## :open_file_folder: Project Structure
```
├── BrowserStack_selenium.py             # Runs the complete automation in 5 random devices
└── browserstack_runner.py              # (Optional) config for browsestack session
├── images/                             # (Optional) Directory to save images locally
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```
---
## :rocket: How to Run
### 1. Clone the Repository
```bash
git clone https://github.com/piyushkr0509/Browserstack-selenium-scraper.git
```
### 2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
```
### 3. Export BrowserStack Credentials
```bash
export BROWSERSTACK_USERNAME=your_browserstack_username
export BROWSERSTACK_ACCESS_KEY=your_browserstack_key
```
### 4. Run the Scraper on Random Devices
```bash
python browserstack_runner.py
```
---
## :earth_africa: Test Coverage Matrix (Randomized per Run)
- Windows 10 / Chrome
- macOS Sonoma / Safari
- Windows 11 / Firefox
- Android 13 / Chrome
- iOS 17 / Safari (iPhone 15)
---
## :white_check_mark: Output
- Console logs showing article scraping
- Translation results
- Repeated word analysis
- (Optional) Saved JSON file with articles
---
## :mailbox_with_mail: Author
**Piyush** – Senior Test Automation Engineer
:email: Drop a message if you'd like to collaborate on automation or test strategy!
---
## :page_facing_up: License
MIT License. Feel free to use, modify, and improve.
