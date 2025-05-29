from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service  # ✅ Required
import time

# 1. Open browser with correct driver path
service = Service("C:/Selenium_Tests/chromedriver.exe")
driver = webdriver.Chrome(service=service)  # ✅ Correct way

# 2. Go to your website
driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/list")

# 3. Wait for the page to load
wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Add Article')]")))
driver.save_screenshot("before_click.png")

# 4. Find and click the "Add Article" button using flexible XPath based on button text
add_article_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[.//span[contains(text(), 'Add Article')]]")
))
add_article_button.click()

# 5. Wait for results to show (increase this if the form loads slowly)
time.sleep(50)

# 6. Check if results appear
results = driver.find_elements(By.TAG_NAME, "h3")
if len(results) > 0:
    print("✅ Search results found.")
else:
    print("❌ No results found.")

# 7. Close browser
driver.quit()
