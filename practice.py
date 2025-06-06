"""
This script automates the process of purchasing datacenter packages in the GoProxy admin interface.
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
                    arguments[0].style.border = '2px solid red';
                    arguments[0].style.transition = 'all 0.1s';
                """, login_button)
                time.sleep(0.2)
                
                # Click the button
                login_button.click()
                print("Clicked login button")
                time.sleep(1.5)  # Reduced wait
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

            # Step 4: Wait for manual captcha input and press enter
            print("\nPlease enter the captcha manually and press Enter to continue...")
            input("Press Enter after entering the captcha...")
            
            # Wait for login to complete by waiting for the login form to disappear
            print("Waiting for login to complete...")
            try:
                # Wait for the login form to disappear (indicates successful login)
                self.wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/form')))
                print("Login successful")
            except:
                print("Warning: Could not detect login completion")
            
            # Additional wait to ensure page is ready
            time.sleep(2)  # Reduced wait
            
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

    def human_delay(self, min_seconds=0.2, max_seconds=0.8):
        """Add a random delay to mimic human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def click_element(self, xpath, description):
        """Click an element with optimized method"""
        try:
            # Wait for element and click it
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            
            # Quick visual feedback
            self.driver.execute_script("""
                arguments[0].style.border = '2px solid red';
                arguments[0].style.transition = 'all 0.1s';
            """, element)
            
            time.sleep(0.2)  # Brief pause
            element.click()
            print(f"Clicked {description}")
            time.sleep(0.5)  # Reduced wait
            return True
        except Exception as e:
            print(f"Failed to click {description}: {str(e)}")
            return False

    def enter_text(self, xpath, text, description):
        """Enter text in an input field"""
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            
            # Quick visual feedback
            self.driver.execute_script("""
                arguments[0].style.border = '2px solid blue';
                arguments[0].style.transition = 'all 0.1s';
            """, element)
            
            time.sleep(0.2)
            element.clear()
            element.send_keys(text)
            print(f"Entered {text} in {description}")
            return True
        except Exception as e:
            print(f"Failed to enter text in {description}: {str(e)}")
            return False

    def click_element_optimized(self, xpath, description):
        """Optimized click with fallback methods"""
        try:
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            
            if not element.is_displayed() or not element.is_enabled():
                return False
            
            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.human_delay(0.1, 0.3)
            
            # Try JavaScript click first (most reliable)
            try:
                self.driver.execute_script("arguments[0].click();", element)
                print(f"Clicked {description}")
                return True
            except:
                # Fallback to regular click
                try:
                    element.click()
                    print(f"Clicked {description}")
                    return True
                except:
                    return False
                    
        except Exception as e:
            print(f"Failed to click {description}: {str(e)}")
            return False

    def test_purchase_datacenter_packages(self):
        """Test the purchase of datacenter packages"""
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

            # Step 4: Click set meal button - Enhanced for reliability
            set_meal_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[2]/button[1]'
            
            # Wait for page to be fully loaded and button to be ready
            print("Waiting for set meal button to be ready...")
            try:
                # First ensure the main section is loaded
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section')))
                time.sleep(1)
                
                # Wait for the specific button to be clickable
                set_meal_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, set_meal_xpath)))
                
                # Scroll to ensure button is in view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", set_meal_button)
                time.sleep(0.5)
                
                # Add visual feedback
                self.driver.execute_script("""
                    arguments[0].style.border = '3px solid green';
                    arguments[0].style.backgroundColor = 'rgba(0, 255, 0, 0.2)';
                    arguments[0].style.transition = 'all 0.3s';
                """, set_meal_button)
                time.sleep(0.5)
                
                # Try multiple click methods for reliability
                click_success = False
                
                # Method 1: JavaScript click (most reliable for automation)
                try:
                    self.driver.execute_script("arguments[0].click();", set_meal_button)
                    print("Clicked set meal button using JavaScript")
                    click_success = True
                except Exception as e1:
                    print(f"JavaScript click failed: {e1}")
                    
                    # Method 2: Regular Selenium click
                    try:
                        set_meal_button.click()
                        print("Clicked set meal button using regular click")
                        click_success = True
                    except Exception as e2:
                        print(f"Regular click failed: {e2}")
                        
                        # Method 3: ActionChains click
                        try:
                            actions = ActionChains(self.driver)
                            actions.move_to_element(set_meal_button).click().perform()
                            print("Clicked set meal button using ActionChains")
                            click_success = True
                        except Exception as e3:
                            print(f"ActionChains click failed: {e3}")
                
                if not click_success:
                    raise Exception("All click methods failed for set meal button")
                
                # Wait for the modal/form to appear after clicking
                print("Waiting for form to appear after clicking set meal button...")
                try:
                    # Wait for the form container to appear
                    self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/div[6]')))
                    time.sleep(1)
                    print("Form appeared successfully")
                except Exception as e:
                    print(f"Warning: Could not confirm form appearance: {e}")
                    
            except Exception as e:
                print(f"Failed to click set meal button: {str(e)}")
                raise Exception("Failed to click set meal button")

            # Step 5: Click subscription type dropdown
            subscription_type_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[1]/div/div/div/input'
            if not self.click_element(subscription_type_xpath, "subscription type dropdown"):
                raise Exception("Failed to click subscription type dropdown")

            # Wait for dropdown to open
            time.sleep(1)

            # Step 6: Select 动态移动套餐 (Datacenter Package) - Optimized
            datacenter_option_found = False
            datacenter_xpaths = [
                '//li[contains(text(), "动态移动套餐")]',  # By text - most reliable
                '//html/body/div[6]/div[1]/div[1]/ul/li[4]',   # Specific path
                '//span[contains(text(), "动态移动套餐")]'  # By span text
            ]
            
            for xpath in datacenter_xpaths:
                try:
                    element = self.driver.find_element(By.XPATH, xpath)
                    if element.is_displayed():
                        self.driver.execute_script("arguments[0].click();", element)
                        print("Selected 动态移动套餐")
                        datacenter_option_found = True
                        break
                except:
                    continue
            
            if not datacenter_option_found:
                raise Exception("Failed to select 动态移动套餐")

            # Step 7: Click second dropdown
            second_dropdown_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[2]/div/div/div/input'
            if not self.click_element(second_dropdown_xpath, "second dropdown"):
                raise Exception("Failed to click second dropdown")

            # Wait for dropdown to open
            time.sleep(1)

            # Step 8: Select 非自动订阅 (Non-Auto Subscription) from the dropdown (robust method)
            try:
                print("Selecting 非自动订阅 (Non-Auto Subscription)...")
                # Find all visible dropdowns
                dropdowns = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'el-select-dropdown__list')]")
                found = False
                for dropdown in dropdowns:
                    if dropdown.is_displayed():
                        options = dropdown.find_elements(By.TAG_NAME, "li")
                        for option in options:
                            if "非自动订阅" in option.text:
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                                time.sleep(0.2)
                                self.driver.execute_script("arguments[0].click();", option)
                                print("Successfully selected 非自动订阅")
                                found = True
                                break
                        if found:
                            break
                if not found:
                    raise Exception("Could not find 非自动订阅 option in dropdown")
                time.sleep(0.5)
            except Exception as e:
                print(f"Failed to select 非自动订阅: {e}")
                raise Exception("Failed to select 非自动订阅 in second dropdown")

            # Step 9: Click third dropdown 
            third_dropdown_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[3]/div/div/div/input'
            if not self.click_element(third_dropdown_xpath, "third dropdown"):
                raise Exception("Failed to click third dropdown")

            time.sleep(1)

            # Step 10: Select second option from third dropdown
            third_option_xpath = '/html/body/div[5]/div[1]/div[1]/ul/li[2]/span'
            if not self.click_element(third_option_xpath, "second option from third dropdown"):
                raise Exception("Failed to select second option from third dropdown")

            # Step 12: Click text box and enter 2
            text_box_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[5]/div/div/input'
            if not self.enter_text(text_box_xpath, "2", "text box"):
                raise Exception("Failed to enter 2 in text box")
     
            # Step 13: Click confirm button
            confirm_button_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[3]/span/button[2]'
            if not self.click_element_optimized(confirm_button_xpath, "confirm button"):
                if not self.click_element(confirm_button_xpath, "confirm button fallback"):
                    raise Exception("Failed to click confirm button")

            # Wait for popup to close
            time.sleep(2)

            # Step 14: Click payment confirm button
            payment_confirm_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[4]/div[2]/div[1]/div/div[3]/table/tbody/tr[1]/td[19]/div/div/div/button[1]'
            try:
                # Wait for table and find button
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/section/div/div[2]/div[4]/div[2]/div[1]/div/div[3]/table')))
                payment_button = self.wait.until(EC.presence_of_element_located((By.XPATH, payment_confirm_xpath)))
                
                # Scroll and click
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", payment_button)
                time.sleep(0.5)
                payment_button.click()
                print("Clicked payment confirm button")
                
            except Exception as e:
                print(f"Failed to click payment confirm button: {e}")
                raise Exception("Failed to click payment confirm button")

            # Step 15: Click sure button in popup
            sure_button_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[4]/div[3]/div/div/div[3]/span/button[2]'
            try:
                sure_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, sure_button_xpath)))
                sure_button.click()
                print("Clicked sure button in popup")
            except Exception as e:
                print(f"Failed to click sure button: {e}")
                raise Exception("Failed to click sure button")

            time.sleep(1)

            print("✅ Test completed successfully!")
            print("🌐 Browser will remain open for inspection.")
            print("📋 You can manually verify the results and close the browser when done.")
            print("🚫 The browser will NOT close automatically.")
            
            # Keep the script alive to prevent browser from closing
            print("\n⏸️  SCRIPT PAUSED - Browser will stay open")
            print("🔍 You can now manually inspect the results")
            input("🔴 Press Enter when you want to close the browser and exit the script...")

        except Exception as e:
            print(f"Test failed: {str(e)}")
            print("\n⏸️  SCRIPT PAUSED - Browser will stay open for debugging")
            print("🔍 You can manually inspect the error state")
            input("🔴 Press Enter when you want to close the browser and exit the script...")
            raise

    def _select_dropdown_option_by_text(self, dropdown_xpath, option_text, description):
        """Select an option from a dropdown by its visible text"""
        try:
            # Click the dropdown to open it
            self.click_element(dropdown_xpath, f"{description} dropdown")

            # Find all visible dropdowns
            dropdowns = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'el-select-dropdown__list')]")

            found_option = False
            for dropdown_container in dropdowns:
                if not dropdown_container.is_displayed():
                    continue
                try:
                    # Search for the option within this visible dropdown
                    option_to_click = dropdown_container.find_element(By.XPATH, f".//li[.//span[contains(text(), '{option_text}')] or contains(text(), '{option_text}')]")
                    if option_to_click.is_displayed():
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option_to_click)
                        self.human_delay(0.1, 0.3)
                        self._highlight_element(option_to_click, color="purple")
                        option_to_click.click()
                        print(f"Selected '{option_text}' from {description} dropdown.")
                        found_option = True
                        break
                except Exception:
                    continue # Option not in this dropdown or not interactable
            
            if not found_option:
                print(f"Could not find '{option_text}' in {description} dropdown.")
                return False
            return True
        except Exception as e:
            print(f"Failed to select option from {description} dropdown: {str(e)}")
            return False

if __name__ == '__main__':
    unittest.main(verbosity=2) 