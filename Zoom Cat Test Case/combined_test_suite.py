import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time
import os
from datetime import datetime
import random
import string

class CombinedTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup test environment once before all tests"""
        # Setup directories
        cls.screenshot_dir = "test_screenshots"
        cls.reports_dir = "C:/Selenium_Tests/Reports"
        os.makedirs(cls.screenshot_dir, exist_ok=True)
        os.makedirs(cls.reports_dir, exist_ok=True)
        
        # Create report file
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        cls.report_file = os.path.join(cls.reports_dir, f"combined_test_suite_{current_time}.txt")
        
        with open(cls.report_file, "w", encoding="utf-8") as f:
            f.write(f"Combined Test Suite Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*50}\n\n")

        # Setup browser
        cls.driver = webdriver.Chrome(service=Service("C:/Selenium_Tests/chromedriver.exe"))
        cls.wait = WebDriverWait(cls.driver, 20)

    def setUp(self):
        """Setup before each test method"""
        try:
            print("\nStarting login process...")
            # Navigate to login page
            self.driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/categorization")
            print("Navigated to login page")
            time.sleep(5)  # Wait for QR code to appear
            
            # Click login button
            print("Looking for login button...")
            login_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div/div/div/form/div[2]/div/div/button')
            ))
            print("Found login button")
            self.highlight_element(login_button, "blue", 1)
            login_button.click()
            print("Clicked login button")
            self.log_step("Clicked login button")
            
            # Enter username
            print("Looking for username input...")
            username_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/form/div[1]/div/div/input')
            ))
            print("Found username input")
            self.highlight_element(username_input, "green", 1)
            username_input.clear()
            username_input.send_keys("nazarabdulsamadbaba")
            print("Entered username")
            self.log_step("Entered username")
            
            # Enter password
            print("Looking for password input...")
            password_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/form/div[2]/div/div/input')
            ))
            print("Found password input")
            self.highlight_element(password_input, "green", 1)
            password_input.clear()
            password_input.send_keys("Samad@2014")
            print("Entered password")
            self.log_step("Entered password")
            
            # Wait for manual captcha entry
            print("Waiting for manual captcha entry (30 seconds)...")
            self.log_step("Waiting for manual captcha entry...")
            time.sleep(30)  # Give time for manual captcha entry
            
            # After manual captcha entry, the page will automatically proceed
            print("Login process completed")
            self.log_step("Login process completed")
            
        except Exception as e:
            print(f"\nERROR in setUp: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            self.take_screenshot("login_error")
            self.log_step(f"Login failed: {str(e)}", "FAIL")
            raise

    @classmethod
    def tearDownClass(cls):
        """Cleanup after all tests are complete"""
        try:
            # Close browser
            if hasattr(cls, 'driver'):
                cls.driver.quit()
            
            # Clean up old screenshots
            if os.path.exists(cls.screenshot_dir):
                screenshots = sorted([f for f in os.listdir(cls.screenshot_dir) if f.endswith('.png')])
                if len(screenshots) > 5:
                    for old_screenshot in screenshots[:-5]:
                        os.remove(os.path.join(cls.screenshot_dir, old_screenshot))
            
            # Clean up old reports
            if os.path.exists(cls.reports_dir):
                report_files = sorted([f for f in os.listdir(cls.reports_dir) 
                                    if f.startswith('combined_test_suite_') and f.endswith('.txt')])
                if len(report_files) > 5:
                    for old_report in report_files[:-5]:
                        os.remove(os.path.join(cls.reports_dir, old_report))
                    
        except Exception as e:
            print(f"Cleanup error: {str(e)}")

    def tearDown(self):
        """Cleanup after each test method"""
        try:
            print("\nClosing browser...")
            if hasattr(self, 'driver'):
                self.driver.quit()
            print("Browser closed successfully")
        except Exception as e:
            print(f"Error closing browser: {str(e)}")

    def generate_random_name(self, prefix="test", length=8):
        """Generate a random name for testing"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        timestamp = datetime.now().strftime('%H%M%S')
        return f"{prefix}_{random_str}_{timestamp}"

    def generate_random_words(self, count):
        """Generate random words for testing"""
        words = ['test', 'article', 'content', 'sample', 'random', 'example', 'data', 'text', 'word', 'sentence',
                'paragraph', 'story', 'news', 'update', 'information', 'details', 'description', 'summary', 'note']
        return ' '.join(random.choices(words, k=count))

    def highlight_element(self, element, color="red", duration=1):
        """Highlight an element with a colored border"""
        original_style = element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid " + color + "';"
            "arguments[0].style.borderRadius='50%';"
            "arguments[0].style.padding='5px';",
            element
        )
        self.take_screenshot(f"highlight_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        time.sleep(duration)
        self.driver.execute_script(
            "arguments[0].style='" + original_style + "';",
            element
        )

    def take_screenshot(self, step):
        """Take a screenshot of the current state"""
        self.driver.save_screenshot(f"{self.screenshot_dir}/{step}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

    def log_step(self, step, status="PASS"):
        """Log a test step with timestamp"""
        with open(self.report_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {step}: {status}\n")

    def test_article_category_creation(self):
        """Test creating a new article category"""
        try:
            self.log_step("Starting Article Category Creation Test")
            # Navigate to category page
            self.driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/categorization")
            time.sleep(5)  # Wait for page to load

            # Generate random test name
            test_name = self.generate_random_name()
            self.log_step(f"Generated test name: {test_name}")

            # Click add button
            add_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/form/button[2]/span")
            ))
            self.highlight_element(add_button, "blue", 1)
            add_button.click()
            self.take_screenshot("1_add_clicked")
            self.log_step("Clicked Add button")

            # Enter category name
            name_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[2]/div/div[1]/input")
            ))
            self.highlight_element(name_input, "green", 1)
            name_input.clear()
            name_input.send_keys(test_name)
            self.take_screenshot("2_name_entered")
            self.log_step(f"Entered category name: {test_name}")

            # Enter sorting number
            sort_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[3]/div/div/input")
            ))
            self.highlight_element(sort_input, "green", 1)
            sort_input.clear()
            sort_input.send_keys("1")
            self.take_screenshot("3_sort_entered")
            self.log_step("Entered sorting number")

            # Click confirm
            confirm_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[3]/div/button[2]/span")
            ))
            self.highlight_element(confirm_button, "blue", 1)
            confirm_button.click()
            self.take_screenshot("4_confirmed")
            self.log_step("Clicked confirm")

            # Verify success
            table = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[1]/div[3]/table")
            ))
            self.highlight_element(table, "yellow", 1)
            self.take_screenshot("5_verified")
            self.log_step("Article category creation completed successfully")

        except Exception as e:
            self.take_screenshot("error")
            self.log_step(f"Article category creation failed: {str(e)}", "FAIL")
            raise

    def test_article_creation(self):
        """Test creating a new article"""
        try:
            self.log_step("Starting Article Creation Test")
            self.driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/list")
            
            # Generate random content
            random_title = self.generate_random_name(prefix="title")
            random_summary = self.generate_random_words(5)
            random_content = self.generate_random_words(10)
            
            self.log_step(f"Generated random content - Title: {random_title}")

            # Click Add Article button
            add_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/form/button[2]/span")
            ))
            self.highlight_element(add_button, "blue", 1)
            add_button.click()
            self.take_screenshot("1_add_clicked")
            self.log_step("Clicked Add Article button")

            # Select category
            category_dropdown = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[2]/div/div/div/input")
            ))
            self.highlight_element(category_dropdown, "green", 1)
            category_dropdown.click()
            time.sleep(1)

            category_option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[4]/div[1]/div[1]/ul/li[6]")
            ))
            self.highlight_element(category_option, "blue", 1)
            category_option.click()
            self.take_screenshot("2_category_selected")
            self.log_step("Selected article category")

            # Enter title
            title_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[3]/div/div[1]/input")
            ))
            self.highlight_element(title_input, "green", 1)
            title_input.clear()
            title_input.send_keys(random_title)
            self.take_screenshot("3_title_entered")
            self.log_step(f"Entered title: {random_title}")

            # Enter summary
            summary_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[4]/div/div[1]/textarea")
            ))
            self.highlight_element(summary_input, "green", 1)
            summary_input.clear()
            summary_input.send_keys(random_summary)
            self.take_screenshot("4_summary_entered")
            self.log_step(f"Entered summary: {random_summary}")

            # Enter content
            content_input = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[2]/form/div[5]/div/div/div[1]/div[2]/div[1]")
            ))
            self.highlight_element(content_input, "green", 1)
            content_input.click()
            time.sleep(1)

            try:
                iframe = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tox-edit-area__iframe")))
                self.driver.switch_to.frame(iframe)
                editable_body = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                self.highlight_element(editable_body, "green", 1)
                editable_body.clear()
                editable_body.send_keys(random_content)
                self.driver.switch_to.default_content()
            except Exception as e:
                self.log_step(f"Failed to enter content in iframe: {str(e)}", "WARNING")
                content_input.clear()
                content_input.send_keys(random_content)

            self.take_screenshot("5_content_entered")
            self.log_step(f"Entered content: {random_content}")

            # Submit form
            submit_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='app']/div/div[2]/section/section/div/div/div[2]/div/div[3]/div/button[2]/span")
            ))
            self.highlight_element(submit_button, "blue", 1)
            submit_button.click()
            self.take_screenshot("6_submitted")
            self.log_step("Clicked submit button")

            # Verify success
            time.sleep(2)
            self.take_screenshot("7_verified")
            self.log_step("Article creation completed successfully")

        except Exception as e:
            self.take_screenshot("error")
            self.log_step(f"Article creation failed: {str(e)}", "FAIL")
            raise

    def test_view_complaints(self):
        """Test viewing complaints in the admin backend"""
        try:
            self.log_step("Starting Complaints View Test")
            self.driver.get("https://test-admin-ipipgo.cd.xiaoxigroup.net/app-manager/operational/article/complain")
            time.sleep(5)

            # Wait for the complaints table to be visible
            complaints_table = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'el-table')]")
            ))
            self.highlight_element(complaints_table, "green", 1)
            self.take_screenshot("complaints_table_visible")
            self.log_step("Complaints table is visible")

            # Verify table headers
            headers = self.driver.find_elements(By.XPATH, "//th[contains(@class, 'el-table__cell')]")
            expected_headers = ["Complaint ID", "User", "Type", "Status", "Created Date", "Actions"]
            
            for header, expected in zip(headers, expected_headers):
                if header.text.strip() == expected:
                    self.highlight_element(header, "blue", 1)
                    self.log_step(f"Found header: {expected}")
                else:
                    raise AssertionError(f"Expected header '{expected}' not found")

            self.take_screenshot("headers_verified")
            self.log_step("All headers verified successfully")
            self.log_step("Complaints view test completed successfully")

        except Exception as e:
            self.take_screenshot("error")
            self.log_step(f"Complaints view test failed: {str(e)}", "FAIL")
            raise

if __name__ == '__main__':
    unittest.main(verbosity=2) 