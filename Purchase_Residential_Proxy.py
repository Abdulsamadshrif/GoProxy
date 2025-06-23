"""
This script automates the process of purchasing dynamic packages in the GoProxy admin interface.
It performs the following steps:
1. Navigates to the customer list page
2. Searches for a specific user ID
3. Performs top-up operation (currently disabled)
4. Sets up a package with specific parameters
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

# Configuration values
ADMIN_URL = "https://test-admin-goproxy.xiaoxitech.com/customer/customerList"
USERNAME = "nazarabdulsamadbaba"
PASSWORD = "Samad@2014"
USER_DETAILS_URL = "https://test-admin-goproxy.xiaoxitech.com/customer/userList/customerDetails?id=853&brand=goproxy"
TOPUP_AMOUNT = "100"

# Feature flags
ENABLE_TOPUP = False  # Set to False to disable top-up functionality

class TestGoProxyPurchase(unittest.TestCase):
    def setUp(self):
        """Setup before each test"""
        # Create directories for reports
        self.reports_dir = "C:/Selenium_Tests/Reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Create report file
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.report_file = os.path.join(self.reports_dir, f"test_goproxy_purchase_{current_time}.txt")
        
        # Initialize browser
        chrome_options = webdriver.ChromeOptions()
        
        # Add options to make browser less detectable as automation
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Execute script to hide webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.wait = WebDriverWait(self.driver, 20)
        
        # Load the page and login
        self.load_pages()
        self.login()

    def load_pages(self):
        """Load the required pages"""
        # Load customer list page
        self.driver.get(ADMIN_URL)
        # Wait for page to load by checking for a known element
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/form/div[2]/div/div/button')))

    def login(self):
        """Handle login process with manual captcha"""
        try:
            # Wait for login form to be present and clickable
            print("Waiting for login form to load...")
            # First wait for the page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
            
            # Step 1: Click login button first
            login_button_xpath = '//*[@id="app"]/div/div/div/form/div[2]/div/div/button'
            try:
                # Wait for login button to be clickable
                login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
                
                # Add visual feedback - red highlight
                self.driver.execute_script("""
                    arguments[0].style.border = '3px solid red';
                    arguments[0].style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
                    arguments[0].style.transition = 'all 0.3s';
                """, login_button)
                time.sleep(0.5)
                
                # Click the button
                login_button.click()
                print("Clicked login button")
                time.sleep(2)  # Wait for login form to appear
            except Exception as e:
                print(f"Failed to click login button: {str(e)}")
                raise

            # Step 2: Enter username
            username_xpath = '//*[@id="app"]/div/div/form/div[1]/div/div/input'
            if not self.enter_text(username_xpath, USERNAME, "username field"):
                raise Exception("Failed to enter username")

            # Step 3: Enter password
            password_xpath = '//*[@id="app"]/div/div/form/div[2]/div/div[1]/input'
            if not self.enter_text(password_xpath, PASSWORD, "password field"):
                raise Exception("Failed to enter password")

            # Step 4: Click CAPTCHA text box and wait for manual input
            captcha_xpath = '//*[@id="app"]/div/div/form/div[3]/div/div/div[1]/input'
            if not self.click_element(captcha_xpath, "captcha text box"):
                raise Exception("Failed to click captcha text box")
            
            print("\nPlease enter the captcha manually and click Enter in the browser...")
            
            # Wait for login to complete by waiting for the login form to disappear
            print("Waiting for login to complete...")
            try:
                # Wait for the login form to disappear (indicates successful login)
                self.wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/form')))
                print("Login successful")
            except:
                print("Warning: Could not detect login completion")
            
            # Additional wait to ensure page is ready
            time.sleep(3)
            
            # Now navigate to user details page
            print("Navigating to user details page...")
            self.driver.get(USER_DETAILS_URL)
            
            # Wait for the page to load
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/div[2]/button[2]')))
                print("Successfully navigated to user details page")
            except Exception as e:
                print(f"Warning: Could not verify page load: {str(e)}")

        except Exception as e:
            print(f"Login failed: {str(e)}")
            # Take screenshot for debugging
            raise

    def tearDown(self):
        """Cleanup after test"""
        # Do NOT close the browser
        print("\nTest completed. Browser will remain open for manual inspection.")
        print("You can close the browser manually when you're done.")
        pass

    def human_delay(self, min_seconds=0.5, max_seconds=2.0):
        """Add a random delay to mimic human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        print(f"Human-like delay: {delay:.2f} seconds")
        time.sleep(delay)

    def click_element(self, xpath, description):
        """Click an element with retry mechanism"""
        try:
            # Wait for element and click it
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            
            # Add visual feedback - red border and background
            self.driver.execute_script("""
                arguments[0].style.border = '3px solid red';
                arguments[0].style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
                arguments[0].style.transition = 'all 0.3s';
            """, element)
            
            # Add a red triangle pointer
            self.driver.execute_script("""
                var triangle = document.createElement('div');
                triangle.style.width = '0';
                triangle.style.height = '0';
                triangle.style.borderLeft = '20px solid transparent';
                triangle.style.borderRight = '20px solid transparent';
                triangle.style.borderTop = '20px solid red';
                triangle.style.position = 'absolute';
                var rect = arguments[0].getBoundingClientRect();
                triangle.style.left = (rect.left + rect.width/2 - 20) + 'px';
                triangle.style.top = (rect.top - 25) + 'px';
                triangle.style.zIndex = '9999';
                triangle.id = 'clickTriangle';
                document.body.appendChild(triangle);
                setTimeout(function() {
                    var el = document.getElementById('clickTriangle');
                    if(el) el.remove();
                }, 2000);
            """, element)
            
            time.sleep(0.5)  # Brief pause to show the highlight
            
            element.click()
            print(f"Clicked {description}")
            # Small wait for any animations
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Failed to click {description}: {str(e)}")
            return False

    def enter_text(self, xpath, text, description):
        """Enter text in an input field"""
        try:
            # Wait for input field and enter text
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            
            # Add visual feedback - blue border for input fields
            self.driver.execute_script("""
                arguments[0].style.border = '3px solid blue';
                arguments[0].style.backgroundColor = 'rgba(0, 0, 255, 0.1)';
                arguments[0].style.transition = 'all 0.3s';
            """, element)
            
            time.sleep(0.5)  # Brief pause to show the highlight
            
            element.clear()
            element.send_keys(text)
            print(f"Entered {text} in {description}")
            # Wait for any dynamic content to update
            self.wait.until(lambda driver: element.get_attribute('value') == text)
            return True
        except Exception as e:
            print(f"Failed to enter text in {description}: {str(e)}")
            return False

    def click_element_human_like(self, xpath, description):
        """Click element with human-like behavior - focus, hover, multiple methods"""
        print(f"Attempting human-like click for {description}")
        
        try:
            # Wait for element to be present
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            
            # Check if element is actually visible and enabled
            if not element.is_displayed():
                print(f"Element {description} is not visible")
                return False
                
            if not element.is_enabled():
                print(f"Element {description} is not enabled")
                return False
            
            # Scroll element into view
            print(f"Scrolling {description} into view...")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
            self.human_delay(0.3, 0.8)
            
            # Focus the element first (triggers focus events)
            print(f"Focusing {description}...")
            self.driver.execute_script("arguments[0].focus();", element)
            self.human_delay(0.2, 0.5)
            
            # Move mouse to element (triggers hover events)
            print(f"Moving mouse to {description}...")
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self.human_delay(0.3, 0.7)
            
            # Add visual feedback
            self.driver.execute_script("""
                arguments[0].style.border = '3px solid green';
                arguments[0].style.backgroundColor = 'rgba(0, 255, 0, 0.3)';
                arguments[0].style.transition = 'all 0.3s';
            """, element)
            time.sleep(0.5)
            
            # Method 1: Try regular Selenium click first
            print(f"Trying regular click for {description}...")
            try:
                element.click()
                print(f"Regular click successful for {description}")
                return True
            except Exception as e1:
                print(f"Regular click failed: {e1}")
                
                # Method 2: Try JavaScript click
                print(f"Trying JavaScript click for {description}...")
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    print(f"JavaScript click successful for {description}")
                    return True
                except Exception as e2:
                    print(f"JavaScript click failed: {e2}")
                    
                    # Method 3: Try ActionChains click
                    print(f"Trying ActionChains click for {description}...")
                    try:
                        actions = ActionChains(self.driver)
                        actions.click(element).perform()
                        print(f"ActionChains click successful for {description}")
                        return True
                    except Exception as e3:
                        print(f"ActionChains click failed: {e3}")
                        
                        # Method 4: Try sending ENTER key
                        print(f"Trying ENTER key for {description}...")
                        try:
                            element.send_keys(Keys.RETURN)
                            print(f"ENTER key successful for {description}")
                            return True
                        except Exception as e4:
                            print(f"ENTER key failed: {e4}")
                            
            return False
            
        except Exception as e:
            print(f"Failed to find element {description}: {str(e)}")
            return False

    def test_purchase_dynamic_packages(self):
        """Test the purchase of dynamic packages"""
        try:
            # Top-up functionality (currently disabled)
            if ENABLE_TOPUP:
                # Step 1: Click Top up button
                top_up_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[2]/button[2]'
                if not self.click_element(top_up_xpath, "Top up button"):
                    raise Exception("Failed to click Top up button")

                # Wait for the amount field to appear after clicking Top up
                amount_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[5]/div/div/div[2]/div/form/div/div/div[1]/input'
                try:
                    print("Waiting for amount field to appear...")
                    self.wait.until(EC.presence_of_element_located((By.XPATH, amount_xpath)))
                    time.sleep(1)  # Additional wait for field to be ready
                    print("Amount field found")
                except Exception as e:
                    print(f"Amount field not found: {str(e)}")
                    
                # Step 2: Enter amount
                if not self.enter_text(amount_xpath, TOPUP_AMOUNT, "amount field"):
                    raise Exception("Failed to enter amount")
                
                # Step 3: Click confirm button
                confirm_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[5]/div/div/div[3]/span/button[2]'
                if not self.click_element(confirm_xpath, "confirm button"):
                    raise Exception("Failed to click confirm button")
            else:
                print("Top-up functionality is disabled")

            # Step 4: Click set meal button
            set_meal_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[2]/button[1]'
            if not self.click_element(set_meal_xpath, "set meal button"):
                raise Exception("Failed to click set meal button")

            # Step 5: Select subscription type
            subscription_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[2]/div/div/div/input'
            if not self.click_element(subscription_xpath, "subscription dropdown"):
                raise Exception("Failed to click subscription dropdown")

            # Add wait time for dropdown to fully open
            print("Waiting for subscription dropdown to open...")
            time.sleep(2)

            # Step 6: Select 非自动订阅 (Non-Auto Subscription)
            try:
                print("Attempting to select 非自动订阅 (Non-Auto Subscription)...")
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "el-select-dropdown__item")))
                dropdown_items = self.driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")
                target_text = "非自动订阅"  # Non-Auto Subscription in Chinese
                no_auto_element = None
                for item in dropdown_items:
                    if target_text in item.text:
                        no_auto_element = item
                        break
                if no_auto_element:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", no_auto_element)
                    time.sleep(0.5)
                    no_auto_element.click()
                    print("Clicked 非自动订阅 (Non-Auto Subscription) option")
                else:
                    raise Exception("Failed to find 非自动订阅 (Non-Auto Subscription) option")
                time.sleep(1)  # Wait for selection to take effect
            except Exception as e:
                print(f"Error selecting 非自动订阅: {str(e)}")
                raise Exception("Failed to select 非自动订阅 (Non-Auto Subscription)")
                            
            # Step 7: Select package size
            package_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[3]/div/div/div/input'
            if not self.click_element(package_xpath, "package size dropdown"):
                raise Exception("Failed to click package size dropdown")

            # CRITICAL: Wait for dropdown to fully open
            print("Waiting for dropdown to open...")
            time.sleep(2)
            
            # Step 8: Select 1GB option
            one_gb_xpath = '/html/body/div[5]/div[1]/div[1]/ul/li[44]'  # 1GB is the 44th option
            # Try with explicit wait for this specific element
            try:
                print("Waiting for 1GB option to be clickable...")
                
                # Try to find and scroll to 1GB option
                try:
                    # Find all dropdown options currently visible
                    all_options = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'el-select-dropdown__list')]//li")
                    print(f"Found {len(all_options)} options in dropdown")
                    
                    # Find the 1GB option
                    one_gb_element = None
                    for option in all_options:
                        if option.text == "1GB":
                            one_gb_element = option
                            print("Found 1GB option")
                            break
                    
                    if one_gb_element:
                        # Scroll to the element
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", one_gb_element)
                        time.sleep(0.5)  # Wait for scroll to complete
                        
                        # Add visual feedback before clicking
                        self.driver.execute_script("""
                            arguments[0].style.border = '3px solid red';
                            arguments[0].style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
                            arguments[0].style.transition = 'all 0.3s';
                        """, one_gb_element)
                        time.sleep(0.5)
                        
                        # Try clicking with JavaScript
                        self.driver.execute_script("arguments[0].click();", one_gb_element)
                        print("Clicked 1GB option using JavaScript")
                    else:
                        print("1GB option not found in current dropdown")
                        raise Exception("1GB option not found")
                        
                except Exception as e:
                    print(f"Failed with scrolling method: {e}")
                    # Try alternative approach - find visible dropdown and click 44th item
                    try:
                        # Find the visible dropdown
                        visible_dropdown = self.driver.find_element(By.XPATH, "//div[contains(@class, 'el-select-dropdown') and not(contains(@style, 'display: none'))]//ul")
                        # Scroll within the dropdown to the 44th item
                        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight * 0.5;", visible_dropdown)
                        time.sleep(0.5)
                        
                        # Now try to click the 1GB option
                        one_gb = self.driver.find_element(By.XPATH, "//li[text()='1GB']")
                        
                        # Add visual feedback before clicking
                        self.driver.execute_script("""
                            arguments[0].style.border = '3px solid red';
                            arguments[0].style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
                            arguments[0].style.transition = 'all 0.3s';
                        """, one_gb)
                        time.sleep(0.5)
                        
                        self.driver.execute_script("arguments[0].click();", one_gb)
                        print("Clicked 1GB after scrolling dropdown")
                    except Exception as e2:
                        print(f"Alternative method also failed: {e2}")
                        # Take screenshot to debug
                        raise Exception("Failed to select 1GB option")
                        
            except Exception as e:
                print(f"Failed to click 1GB option: {str(e)}")
                raise Exception("Failed to select 1GB option")

            # Step 9: Enter duration
            duration_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[5]/div/div[1]/input'
            
            # Wait for form to be ready after package selection
            print("Waiting for duration field to be ready after package selection...")
            time.sleep(3)
            
            # Verify the duration field is available and ready
            try:
                duration_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, duration_xpath)))
                print("Duration field is ready and clickable")
            except Exception as e:
                print(f"Duration field not ready: {e}")
            
            if not self.enter_text(duration_xpath, "7", "duration field"):
                raise Exception("Failed to enter duration")
            
            # Ensure form is fully processed before confirming
            print("Waiting for form to process duration entry...")
            time.sleep(2)

            # Step 10: Confirm package setup
            final_confirm_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[3]/span/button[2]'
            
            # Robust retry mechanism for intermittent timing issues
            confirm_success = False
            max_attempts = 5
            
            for attempt in range(max_attempts):
                print(f"Attempting to click final confirm button (attempt {attempt + 1}/{max_attempts})")
                
                try:
                    # Wait a bit longer each attempt
                    wait_time = 2 + (attempt * 1)  # 2, 3, 4, 5, 6 seconds
                    print(f"Waiting {wait_time} seconds for form to be ready...")
                    time.sleep(wait_time)
                    
                    # Try to click the button with human-like behavior
                    if self.click_element_human_like(final_confirm_xpath, f"final confirm button (attempt {attempt + 1})"):
                        confirm_success = True
                        print("Successfully clicked final confirm button with human-like method!")
                        break
                    # Fallback to regular click if human-like fails
                    elif self.click_element(final_confirm_xpath, f"final confirm button fallback (attempt {attempt + 1})"):
                        confirm_success = True
                        print("Successfully clicked final confirm button with fallback method!")
                        break
                    else:
                        print(f"Attempt {attempt + 1} failed, trying alternative methods...")
                        
                        # Try alternative selectors on failed attempts
                        if attempt >= 2:  # After 2 failed attempts, try alternatives
                            print("Trying alternative selectors with human-like clicks...")
                            alternative_selectors = [
                                '//button[contains(text(), "确定")]',  # Chinese "OK"
                                '//button[contains(text(), "确认")]',  # Chinese "Confirm"
                                '//span[contains(@class, "el-dialog__footer")]//button[last()]',  # Last button in dialog footer
                                '//div[contains(@class, "el-dialog")]//button[@type="button"][last()]'  # Last button in dialog
                            ]
                            
                            for alt_selector in alternative_selectors:
                                print(f"Trying alternative selector with human-like click: {alt_selector}")
                                if self.click_element_human_like(alt_selector, f"final confirm button (alternative)"):
                                    confirm_success = True
                                    print("Successfully clicked with alternative selector and human-like method!")
                                    break
                            
                            if confirm_success:
                                break
                except Exception as e:
                    print(f"Exception on attempt {attempt + 1}: {str(e)}")
            
            if not confirm_success:
                # Final attempt - take screenshot and show debug info
                print("All attempts failed.")
                
                # Show available buttons for debugging
                try:
                    buttons = self.driver.find_elements(By.XPATH, "//button")
                    print(f"Found {len(buttons)} buttons on page:")
                    for i, btn in enumerate(buttons[:5]):  # Show first 5 buttons
                        try:
                            if btn.is_displayed():
                                print(f"  Button {i+1}: text='{btn.text}', class='{btn.get_attribute('class')}'")
                        except:
                            continue
                except Exception as e:
                    print(f"Could not enumerate buttons: {e}")
                
                raise Exception("Failed to click final confirm button after all attempts")
            
            # Step 11: Click confirm payment button in table
            confirm_payment_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[4]/div[2]/div[1]/div/div[3]/table/tbody/tr[1]/td[19]/div/div/div/button[1]'
            try:
                print("Looking for confirm payment button in table...")
                # Wait for the table to be present
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/div[4]/div[2]/div[1]/div/div[3]/table')))
                time.sleep(1)
                
                # Find and scroll to the button (it's in column 19, likely off-screen)
                confirm_payment_button = self.wait.until(EC.presence_of_element_located((By.XPATH, confirm_payment_xpath)))
                
                # Scroll horizontally and vertically to center the button
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", confirm_payment_button)
                time.sleep(1)
                
                # Add visual feedback
                self.driver.execute_script("""
                    arguments[0].style.border = '3px solid red';
                    arguments[0].style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
                    arguments[0].style.transition = 'all 0.3s';
                """, confirm_payment_button)
                time.sleep(0.5)
                
                # Click the button
                confirm_payment_button.click()
                print("Clicked confirm payment button")
                
            except Exception as e:
                print(f"Failed to click confirm payment button: {e}")
                raise Exception("Failed to click confirm payment button")
            
            # Step 12: Handle popup and click sure button
            sure_button_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[4]/div[3]/div/div/div[3]/span/button[2]'
            try:
                print("Waiting for popup to appear...")
                # Wait for the popup to appear
                sure_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, sure_button_xpath)))
                
                # Add visual feedback
                self.driver.execute_script("""
                    arguments[0].style.border = '3px solid red';
                    arguments[0].style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
                    arguments[0].style.transition = 'all 0.3s';
                    
                    // Also add a triangle pointer
                    var triangle = document.createElement('div');
                    triangle.style.width = '0';
                    triangle.style.height = '0';
                    triangle.style.borderLeft = '20px solid transparent';
                    triangle.style.borderRight = '20px solid transparent';
                    triangle.style.borderTop = '20px solid red';
                    triangle.style.position = 'absolute';
                    var rect = arguments[0].getBoundingClientRect();
                    triangle.style.left = (rect.left + rect.width/2 - 20) + 'px';
                    triangle.style.top = (rect.top - 25) + 'px';
                    triangle.style.zIndex = '99999';
                    triangle.id = 'sureTriangle';
                    document.body.appendChild(triangle);
                    setTimeout(function() {
                        var el = document.getElementById('sureTriangle');
                        if(el) el.remove();
                    }, 2000);
                """, sure_button)
                time.sleep(1)
                
                # Click the sure button
                sure_button.click()
                print("Clicked sure button in popup")
                
            except Exception as e:
                print(f"Failed to click sure button: {e}")
                raise Exception("Failed to click sure button in popup")
                        #//*[@id="app"]/div/div/section/div/div[2]/div[4]/div[2]/div[1]/div/div[3]/table/tbody/tr[1]/td[19]/div/div/div/button[1]
            print("Test completed successfully!")

            # Refresh the page and keep browser open
            self.driver.refresh()
            print("Page refreshed. Browser will remain open. Press Enter in the terminal to close it.")
            input("Press Enter to exit and close the browser...")

        except Exception as e:
            print(f"Test failed: {str(e)}")
            raise

if __name__ == '__main__':
    unittest.main(verbosity=2)
