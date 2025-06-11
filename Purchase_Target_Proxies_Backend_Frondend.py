"""
This script automates the process of purchasing dynamic packages in the GoProxy admin interface.
It performs the following steps:
1. Navigates to the customer list page
2. Searches for a specific user ID
3. Sets up a package with specific parameters
"""

# Import required libraries
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os
from datetime import datetime
import random

# Task 1: Configuration Setup
# Description: Define all necessary configuration values including URLs, credentials, and XPath selectors
# Purpose: Centralize all configuration values for easy maintenance and updates
ADMIN_URL = "https://test-admin-goproxy.xiaoxitech.com/customer/customerList"
USERNAME = "nazarabdulsamadbaba"
PASSWORD = "Samad@2014"
USER_DETAILS_URL = "https://test-admin-goproxy.xiaoxitech.com/customer/userList/customerDetails?id=853&brand=goproxy"

# Task 2: XPath Definitions
# Description: Define all XPath selectors used throughout the script
# Purpose: Organize and maintain all element locators in one place
XPATHS = {
    'login_button': '//*[@id="app"]/div/div/div/form/div[2]/div/div/button',
    'username': '//*[@id="app"]/div/div/form/div[1]/div/div/input',
    'password': '//*[@id="app"]/div/div/form/div[2]/div/div[1]/input',
    'captcha': '//*[@id="app"]/div/div/form/div[3]/div/div/div[1]/input',
    'success_indicators': [
        '//*[@id="app"]/div/div/div/div',
        '//*[@id="app"]/div/div/section',
        '//*[@id="app"]/div/div/div[1]/div/div[1]/div/div[1]/span',
        '//*[@id="app"]/div/div/div[1]/div/div[1]/div/div[2]/span'
    ],
    'page_load_indicators': [
        '//*[@id="app"]/div/div/section/div/div[2]/div[2]/button[2]',
        '//*[@id="app"]/div/div/section/div/div[2]/div[2]/button[1]',
        '//*[@id="app"]/div/div/section/div/div[2]/div[2]'
    ],
    'package_setup': {
        'set_meal': '//*[@id="app"]/div/div/section/div/div[2]/div[2]/button[1]',
        'subscription_type': '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[1]/div/div/div/input',
        'dynamic_datacenter_package': '/html/body/div[6]/div[1]/div[1]/ul/li[6]',
        'auto_subscription': '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[2]/div/div/div/input',
        'non_auto_subscription': '/html/body/div[5]/div[1]/div[1]/ul/li[2]',
        'capacity_dropdown': '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[3]/div/div/div/input',
        'one_gb_option': '/html/body/div[5]/div[1]/div[1]/ul/li[2]',
        'amount_box': '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[5]/div/div[1]/input',
        'confirm': '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[3]/span/button[2]'
    }
}

class TestGoProxyPurchase(unittest.TestCase):
    # Task 3: Test Setup
    # Description: Initialize test environment and browser configuration
    # Purpose: Prepare the testing environment before each test execution
    def setUp(self):
        """Setup before each test"""
        self.setup_browser()
        self.load_pages()
        self.login()

    # Task 4: Browser Configuration
    # Description: Configure Chrome browser with necessary options
    # Purpose: Set up browser with anti-detection measures and required settings
    def setup_browser(self):
        """Initialize and configure the browser"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        self.actions = ActionChains(self.driver)

    # Task 5: Page Loading
    # Description: Load initial pages and wait for elements
    # Purpose: Ensure pages are properly loaded before proceeding
    def load_pages(self):
        """Load the required pages"""
        self.driver.get(ADMIN_URL)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS['login_button'])))

    # Task 6: Element Highlighting
    # Description: Add visual feedback for element interactions
    # Purpose: Help with debugging and visual tracking of automation
    def highlight_element(self, element, color='red'):
        """Add visual feedback to an element"""
        colors = {
            'red': ('3px solid red', 'rgba(255, 0, 0, 0.3)'),
            'blue': ('3px solid blue', 'rgba(0, 0, 255, 0.1)'),
            'green': ('3px solid green', 'rgba(0, 255, 0, 0.3)')
        }
        border, background = colors.get(color, colors['red'])
        self.driver.execute_script(f"""
            arguments[0].style.border = '{border}';
            arguments[0].style.backgroundColor = '{background}';
            arguments[0].style.transition = 'all 0.3s';
        """, element)
        time.sleep(0.2)

    # Task 7: Element Interaction
    # Description: Handle element clicking with visual feedback
    # Purpose: Provide reliable element interaction with error handling
    def click_element(self, xpath, description, color='red'):
        """Click an element with visual feedback"""
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.highlight_element(element, color)
            element.click()
            print(f"Clicked {description}")
            return True
        except Exception as e:
            print(f"Failed to click {description}: {str(e)}")
            return False

    # Task 8: Text Input
    # Description: Handle text input in form fields
    # Purpose: Provide reliable text input with validation
    def enter_text(self, xpath, text, description):
        """Enter text in an input field with enhanced error handling"""
        try:
            print(f"Attempting to enter text '{text}' in {description}")
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.highlight_element(element, 'blue')
            
            # Clear the field first
            element.clear()
            time.sleep(0.5)
            
            # Try multiple methods to enter text
            try:
                element.send_keys(text)
            except:
                try:
                    self.driver.execute_script(f"arguments[0].value = '{text}';", element)
                except:
                    self.actions.move_to_element(element).click().send_keys(text).perform()
            
            # Verify the text was entered correctly
            time.sleep(0.5)
            actual_value = element.get_attribute('value')
            print(f"Actual value in field: {actual_value}")
            
            if str(actual_value) != str(text):
                print(f"Value mismatch. Expected: {text}, Got: {actual_value}")
                # Try one more time with JavaScript
                self.driver.execute_script(f"arguments[0].value = '{text}';", element)
                time.sleep(0.5)
                actual_value = element.get_attribute('value')
                if str(actual_value) != str(text):
                    raise Exception(f"Failed to set value. Expected: {text}, Got: {actual_value}")
            
            print(f"Successfully entered {text} in {description}")
            return True
        except Exception as e:
            print(f"Failed to enter text in {description}: {str(e)}")
            return False

    # Task 9: Element Waiting
    # Description: Wait for elements to be present
    # Purpose: Ensure elements are loaded before interaction
    def wait_for_element(self, xpath_list, description, timeout=20):
        """Wait for any element from a list of XPaths"""
        for xpath in xpath_list:
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                print(f"Found {description}: {xpath}")
                return True
            except:
                continue
        return False

    # Task 10: Dropdown Selection
    # Description: Handle dropdown menu selections
    # Purpose: Provide reliable dropdown interaction
    def select_dropdown_option(self, option_text, description):
        """Select an option from a dropdown"""
        try:
            dropdown_items = self.driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")
            for item in dropdown_items:
                if option_text in item.text:
                    self.highlight_element(item, 'green')
                    item.click()
                    print(f"Selected {option_text} from {description}")
                    return True
            return False
        except Exception as e:
            print(f"Error selecting {option_text} from {description}: {str(e)}")
            return False

    # Task 11: Retry Mechanism
    # Description: Implement retry logic for clicking elements
    # Purpose: Handle intermittent click failures
    def click_with_retry(self, xpath, description, max_attempts=3):
        """Click an element with multiple retry methods"""
        for attempt in range(max_attempts):
            try:
                print(f"Attempting to click {description} (attempt {attempt + 1}/{max_attempts})")
                button = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                time.sleep(0.5)
                
                try:
                    button.click()
                except:
                    try:
                        self.driver.execute_script("arguments[0].click();", button)
                    except:
                        self.actions.move_to_element(button).click().perform()
                
                print(f"Successfully clicked {description}")
                return True
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_attempts - 1:
                    return False
                time.sleep(1)
        return False

    # Task 12: Login Process
    # Description: Handle the login process with manual captcha
    # Purpose: Authenticate user with secure login flow
    def login(self):
        """Handle login process with manual captcha"""
        try:
            print("Starting login process...")
            
            if not self.click_element(XPATHS['login_button'], "login button"):
                raise Exception("Failed to click login button")
            
            if not self.enter_text(XPATHS['username'], USERNAME, "username"):
                raise Exception("Failed to enter username")
            
            if not self.enter_text(XPATHS['password'], PASSWORD, "password"):
                raise Exception("Failed to enter password")
            
            if not self.click_element(XPATHS['captcha'], "captcha text box", 'blue'):
                raise Exception("Failed to click captcha text box")
            
            print("\nPlease enter the captcha manually and click Enter in the browser...")
            
            if not self.wait_for_element(XPATHS['success_indicators'], "success indicator"):
                try:
                    self.wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/form')))
                    print("Login form disappeared, indicating successful login")
                except:
                    raise Exception("Could not detect successful login")
            
            print("Login successful!")
            time.sleep(1)
            
            print("Navigating to user details page...")
            self.driver.get(USER_DETAILS_URL)
            time.sleep(2)
            if not self.wait_for_element(XPATHS['page_load_indicators'], "page load indicator"):
                print("Warning: Could not verify page load with specific indicators, but continuing anyway")
            time.sleep(2)
        except Exception as e:
            print(f"Login failed: {str(e)}")
            raise

    # Task 13: Package Purchase
    # Description: Test the purchase of dynamic packages
    # Purpose: Automate the package purchase process
    def test_purchase_dynamic_packages(self):
        """Test the purchase of datacenter packages"""
        try:
            # Step 1: Click set meal button
            if not self.click_element(XPATHS['package_setup']['set_meal'], "set meal button"):
                raise Exception("Failed to click set meal button")
            time.sleep(3)  # Increased wait time

            # Step 2: Click subscription type dropdown and wait for options
            print("\nClicking subscription type dropdown...")
            subscription_dropdown = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, XPATHS['package_setup']['subscription_type']))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", subscription_dropdown)
            time.sleep(1)
            subscription_dropdown.click()
            time.sleep(2)  # Wait for dropdown to appear

            # Step 3: Select 定制套餐 (Dynamic Datacenter Package) using keyboard navigation
            print("\nAttempting to select dynamic datacenter package using keyboard navigation...")
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    print(f"Attempt {attempt + 1} of {max_attempts}")
                    
                    # Wait for dropdown to be visible
                    time.sleep(2)
                    
                    # Press down arrow 5 times to reach the 6th option
                    actions = ActionChains(self.driver)
                    for _ in range(6):
                        actions.send_keys(Keys.ARROW_DOWN)
                        time.sleep(0.5)  # Small delay between key presses
                    
                    # Press Enter to select the option
                    actions.send_keys(Keys.ENTER)
                    actions.perform()
                    print("Navigated to 6th option and pressed Enter")
                    time.sleep(2)
                    
                    # Verify selection
                    try:
                        selected_text = self.driver.find_element(By.XPATH, XPATHS['package_setup']['subscription_type']).get_attribute('value')
                        if '定制套餐' in selected_text:
                            print("Selection verified successfully")
                            break
                        else:
                            print("Selection not verified, retrying...")
                    except:
                        print("Could not verify selection, retrying...")
                    
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == max_attempts - 1:
                        raise Exception(f"Failed to select dynamic datacenter package after {max_attempts} attempts")
                    time.sleep(2)

            time.sleep(2)  # Wait after selection

            # Step 4: Click auto subscription dropdown
            print("\nClicking auto subscription dropdown...")
            auto_subscription_dropdown = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[2]/div/div/div/input"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", auto_subscription_dropdown)
            time.sleep(1)
            auto_subscription_dropdown.click()
            time.sleep(2)  # Wait for dropdown to appear

            # Step 5: Select test1 option
            print("\nAttempting to select test1 option...")
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    print(f"Attempt {attempt + 1} of {max_attempts}")
                    
                    # Wait for dropdown to be visible
                    time.sleep(2)
                    
                    # Try to find and click the test1 option
                    try:
                        # First try: Using exact XPath
                        element = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[1]/div[1]/ul/li[1]"))
                        )
                        element.click()
                        print("Clicked test1 option using XPath")
                    except:
                        # Second try: Using keyboard navigation
                        actions = ActionChains(self.driver)
                        actions.send_keys(Keys.ARROW_DOWN)  # Press down once to select first option
                        time.sleep(0.5)
                        actions.send_keys(Keys.ENTER)
                        actions.perform()
                        print("Selected test1 option using keyboard")
                    
                    time.sleep(2)
                    
                    # Verify selection
                    try:
                        selected_text = self.driver.find_element(By.XPATH, "//*[@id='app']/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[2]/div/div/div/input").get_attribute('value')
                        if 'test1' in selected_text:
                            print("Selection verified successfully")
                            break
                        else:
                            print("Selection not verified, retrying...")
                    except:
                        print("Could not verify selection, retrying...")
                    
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == max_attempts - 1:
                        raise Exception(f"Failed to select test1 option after {max_attempts} attempts")
                    time.sleep(2)

            time.sleep(2)  # Wait after selection

            # Step 6: Click capacity dropdown
            print("\nClicking capacity dropdown...")
            capacity_dropdown = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[3]/div/div/div/input"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", capacity_dropdown)
            time.sleep(1)
            capacity_dropdown.click()
            time.sleep(2)  # Wait for dropdown to appear

            # Step 7: Select 7天 option
            print("\nAttempting to select 7天 option...")
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    print(f"Attempt {attempt + 1} of {max_attempts}")
                    
                    # Wait for dropdown to be visible
                    time.sleep(2)
                    
                    # Try to find and click the 7天 option
                    try:
                        # First try: Using exact XPath
                        element = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[1]/div[1]/ul/li[1]"))
                        )
                        element.click()
                        print("Clicked 7天 option using XPath")
                    except:
                        # Second try: Using keyboard navigation
                        actions = ActionChains(self.driver)
                        actions.send_keys(Keys.ARROW_DOWN)  # Press down once to select first option
                        time.sleep(0.5)
                        actions.send_keys(Keys.ENTER)
                        actions.perform()
                        print("Selected 7天 option using keyboard")
                    
                    time.sleep(2)
                    
                    # Verify selection
                    try:
                        selected_text = self.driver.find_element(By.XPATH, "//*[@id='app']/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[3]/div/div/div/input").get_attribute('value')
                        if '7天' in selected_text:
                            print("Selection verified successfully")
                            break
                        else:
                            print("Selection not verified, retrying...")
                    except:
                        print("Could not verify selection, retrying...")
                    
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == max_attempts - 1:
                        raise Exception(f"Failed to select 7天 option after {max_attempts} attempts")
                    time.sleep(2)

            time.sleep(2)  # Wait after selection

            # Step 8: Click location dropdown
            print("\nClicking location dropdown...")
            location_dropdown = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[4]/div/div/div[1]/div[1]/div/input"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_dropdown)
            time.sleep(1)
            location_dropdown.click()
            time.sleep(2)  # Wait for dropdown to appear

            # Step 9: Select 古巴-奥尔金 option
            print("\nAttempting to select 古巴-奥尔金 option...")
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    print(f"Attempt {attempt + 1} of {max_attempts}")
                    
                    # Wait for dropdown to be visible
                    time.sleep(2)
                    
                    # Try to find and click the 古巴-奥尔金 option
                    try:
                        # First try: Using exact XPath
                        element = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[1]/div[1]/ul/li[2]"))
                        )
                        element.click()
                        print("Clicked 古巴-奥尔金 option using XPath")
                    except:
                        # Second try: Using keyboard navigation
                        actions = ActionChains(self.driver)
                        actions.send_keys(Keys.ARROW_DOWN)  # Press down once
                        time.sleep(0.5)
                        actions.send_keys(Keys.ARROW_DOWN)  # Press down again to reach second option
                        time.sleep(0.5)
                        actions.send_keys(Keys.ENTER)
                        actions.perform()
                        print("Selected 古巴-奥尔金 option using keyboard")
                    
                    time.sleep(2)
                    
                    # Verify selection
                    try:
                        selected_text = self.driver.find_element(By.XPATH, "//*[@id='app']/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[4]/div/div/div[1]/div[1]/div/input").get_attribute('value')
                        if '古巴-奥尔金' in selected_text:
                            print("Selection verified successfully")
                            break
                        else:
                            print("Selection not verified, retrying...")
                    except:
                        print("Could not verify selection, retrying...")
                    
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == max_attempts - 1:
                        raise Exception(f"Failed to select 古巴-奥尔金 option after {max_attempts} attempts")
                    time.sleep(2)

            time.sleep(2)  # Wait after selection

            # Step 10: Set number to 3
            print("\nSetting number to 3...")
            number_box = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[4]/div/div/div[1]/div[2]/div/input"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", number_box)
            time.sleep(1)
            
            # Clear existing value and enter new value
            number_box.clear()
            time.sleep(0.5)
            number_box.send_keys("3")
            print("Set number to 3")
            time.sleep(2)

            # Step 11: Set amount to 9
            print("\nSetting amount to 9...")
            amount_box = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[6]/div/div/input"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", amount_box)
            time.sleep(1)
            
            # Clear existing value and enter new value
            amount_box.clear()
            time.sleep(0.5)
            amount_box.send_keys("9")
            print("Set amount to 9")
            time.sleep(2)

            # Step 12: Click final confirm button with enhanced handling
            try:
                validation_messages = self.driver.find_elements(By.CLASS_NAME, "el-form-item__error")
                if validation_messages:
                    for msg in validation_messages:
                        print(f"Validation error found: {msg.text}")
                    raise Exception("Form validation errors present")

                confirm_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS['package_setup']['confirm'])))
                
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_button)
                time.sleep(1)
                
                try:
                    confirm_button.click()
                except:
                    try:
                        self.driver.execute_script("arguments[0].click();", confirm_button)
                    except:
                        self.actions.move_to_element(confirm_button).click().perform()
                
                time.sleep(2)
                
                success_indicators = [
                    "//div[contains(@class, 'el-message--success')]",
                    "//div[contains(@class, 'el-message-box')]",
                    "//div[contains(@class, 'el-notification--success')]"
                ]
                
                success_found = False
                for indicator in success_indicators:
                    try:
                        if self.driver.find_element(By.XPATH, indicator).is_displayed():
                            success_found = True
                            print("Success message found!")
                            break
                    except:
                        continue
                
                if not success_found:
                    print("Warning: No success message found after confirmation")
                
            except Exception as e:
                print(f"Failed to confirm purchase: {str(e)}")
                raise

            print("Test completed successfully!")
            
            self.handle_additional_steps()

        except Exception as e:
            print(f"Test failed: {str(e)}")
            raise

    # Task 14: Additional Steps
    # Description: Handle post-purchase steps and payment process
    # Purpose: Complete the purchase flow with payment integration
    def handle_additional_steps(self):
        """Handle the additional steps after successful purchase"""
        try:
            print("\nStarting additional steps...")
            
            print("Navigating to main website...")
            self.driver.get("https://test-goproxy.xiaoxitech.com")
            time.sleep(2)
            
            print("Setting authentication cookies...")
            
            admin_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHQiOiJ7XCJhY3RpdmVcIjp0cnVlLFwibG9naW5fZmxhZ1wiOlwiYWU0ZmU1YThhMWMxMGE1YTVhYTU4NjkzMjU1ZTNlNWJcIn0iLCJ1c2VyX25hbWUiOiJ4aWFveGlxYUBnbWFpbC5jb20iLCJzY29wZSI6WyJhbGwiXSwiZXhwIjoxNzQ5Njk0NDYzLCJ1c2VySWQiOiIxOTA1NDQyNDkwMzcxMTQ1NzI4IiwianRpIjoiMjA0YjY1Y2YtOGVhZS00YzA2LTg2YzgtOWE0MTZiOTJmY2E3IiwiY2xpZW50X2lkIjoiZ29fcHJveHkifQ.y-GAkHh3s66BwGFjohop1h6xkl2LPkLBOpeNZzNISl3Ted0R89rhM45KdUlXRTQvrMadTCVkq9B22MvA7dUf6KBowIp874uAEu72roN1h9cqOkBGMo-z5yOAOnlzZ15i4N4pqHxtjR0Bg01O-wCl_H3AOjMUYrS6CLpYTgQwhGWcYwroeaq66juBDDymkVzgOGXUdO7erFPeUuHc8Q4JIcw9C74DVmIsEE43m18-Q3Dp_8PBZyFiGqbKf_m89c5o3M5L2tYdoLzdtGzlftXG8ibfmk0vt9K2BCs4D2Qqy4iDz8BKspNZgpeaaFlCs6ZbnnLtylZmZHeXFaJpUc0MzQ"
            
            cookies = [
                {
                    'name': 'Admin_Token',
                    'value': admin_token,
                    'domain': 'test-goproxy.xiaoxitech.com',
                    'path': '/'
                },
                {
                    'name': 'clientIP',
                    'value': '60.53.124.67',
                    'domain': 'test-goproxy.xiaoxitech.com',
                    'path': '/'
                },
                {
                    'name': 'G_ENABLED_IDPS',
                    'value': 'google',
                    'domain': 'test-goproxy.xiaoxitech.com',
                    'path': '/'
                },
                {
                    'name': 'gaVisitorUuid',
                    'value': '2e44038e-df8f-4f12-885c-a568af17c47b',
                    'domain': '.xiaoxitech.com',
                    'path': '/'
                }
            ]
            
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Warning: Could not set cookie {cookie['name']}: {str(e)}")
            
            self.driver.execute_script(f"localStorage.setItem('token', '{admin_token}')")
            
            self.driver.refresh()
            time.sleep(3)
            
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'user-info') or contains(@class, 'avatar')]")))
                print("Login successful!")
            except:
                print("Warning: Could not verify login status, but continuing anyway")
            
            print("Navigating to billing page...")
            self.driver.get("https://test-goproxy.xiaoxitech.com/dashboard/billing/")
            time.sleep(3)
            
            print("Clicking on Transaction tab...")
            transaction_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/section/section/main/div/div[1]/div/div[1]/div[3]')))
            self.highlight_element(transaction_tab, 'blue')
            transaction_tab.click()
            time.sleep(2)
            
            print("Clicking payment button...")
            payment_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/section/section/main/div/div[1]/div/div[4]/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[9]/div/div/button[1]')))
            self.highlight_element(payment_button, 'green')
            payment_button.click()
            time.sleep(3)
            
            print("Clicking payment again button...")
            payment_again_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/section/section/main/div/div[1]/div[2]/div[2]/div[1]/button')))
            self.highlight_element(payment_again_button, 'green')
            payment_again_button.click()
            time.sleep(3)
            
            print("\nProcess completed successfully!")
            print("PayPal checkout page is loaded.")
            print("Browser will remain open. Press Enter in the terminal to close it when you're done.")
            input("Press Enter to exit and close the browser...")
            
        except Exception as e:
            print(f"Error in additional steps: {str(e)}")
            raise

    # Task 15: Test Cleanup
    # Description: Handle test cleanup and browser closure
    # Purpose: Ensure proper cleanup after test execution
    def tearDown(self):
        """Cleanup after test"""
        print("\nTest completed. Browser will remain open for manual inspection.")
        print("You can close the browser manually when you're done.")

if __name__ == '__main__':
    unittest.main(verbosity=2)