# GoProxy Dynamic Package Purchase Automation

This project contains Selenium automation scripts for purchasing dynamic packages in the GoProxy admin interface.

## Features

- Automated login with manual captcha handling
- Dynamic package purchase automation
- Top-up operation automation
- Visual feedback during automation
- Screenshot capture on failures
- Detailed logging

## Requirements

- Python 3.x
- Selenium WebDriver
- Chrome Browser
- ChromeDriver

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Selenium_Tests
```

2. Install required packages:
```bash
pip install selenium
```

3. Make sure you have Chrome browser installed

4. Download ChromeDriver matching your Chrome version and add it to your PATH

## Usage

Run the test script:
```bash
python GoProxy/Purchase_Dynamic_packages.py
```

## Project Structure

- `GoProxy/` - Contains the main automation scripts
  - `Purchase_Dynamic_packages.py` - Main test script for package purchase
- `test_screenshots/` - Directory for test screenshots
- `Reports/` - Directory for test reports

## Notes

- The browser will remain open after test completion for manual inspection
- Screenshots are automatically captured on test failures
- Manual captcha input is required during login

## Author

Nazar Abdul Samad 