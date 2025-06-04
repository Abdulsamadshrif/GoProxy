"""
This script automates the process of purchasing static packages in the GoProxy admin interface.
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
        # Create directories for screenshots and reports
        self.screenshot_dir = "test_screenshots"
        self.reports_dir = "C:/Selenium_Tests/Reports"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Create report file
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.report_file = os.path.join(self.reports_dir, f"test_goproxy_purchase_{current_time}.txt")
        
        # Initialize browser
        self.driver = webdriver.Chrome()
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
                self.driver.save_screenshot("login_error.png")
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
                print("Login form disappeared, login successful")
            except:
                print("Warning: Could not detect login form disappearance")
            
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
                self.driver.save_screenshot("page_load_warning.png")

        except Exception as e:
            print(f"Login failed: {str(e)}")
            # Take screenshot for debugging
            self.driver.save_screenshot("login_error.png")
            raise

    def tearDown(self):
        """Cleanup after test"""
        # Do NOT close the browser
        print("\nTest completed. Browser will remain open for manual inspection.")
        print("You can close the browser manually when you're done.")
        pass

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

    def take_screenshot(self, step_name):
        """Take a screenshot with timestamp and step name"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"step_{step_name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        print(f"Screenshot saved: {filepath}")
        return filepath

    def test_purchase_static_packages(self):
        """Test the purchase of static packages"""
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

            # Step 4: Click 'open a set meal' (set meal button)
            set_meal_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[2]/button[1]'
            try:
                print("Clicking set meal button...")
                self.take_screenshot("04a_before_set_meal")
                
                # Wait for button to be clickable
                set_meal_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, set_meal_xpath))
                )
                
                # Scroll button into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", set_meal_button)
                time.sleep(1)
                
                # Try multiple click methods
                try:
                    set_meal_button.click()
                except:
                    try:
                        self.driver.execute_script("arguments[0].click();", set_meal_button)
                    except:
                        ActionChains(self.driver).move_to_element(set_meal_button).click().perform()
                
                self.take_screenshot("04b_after_set_meal_click")
                
                # Wait for the form to appear and be fully loaded
                print("Waiting for set meal form to appear...")
                form_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form'
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, form_xpath))
                )
                
                # Wait for form to be fully interactive
                time.sleep(3)
                self.take_screenshot("04c_form_appeared")
                
                # Verify form is visible and enabled
                form = self.driver.find_element(By.XPATH, form_xpath)
                if not form.is_displayed():
                    raise Exception("Form is not visible after clicking set meal button")
                
                # Additional wait to ensure form is fully loaded
                time.sleep(2)
                
            except Exception as e:
                print(f"Failed in set meal step: {str(e)}")
                self.take_screenshot("04d_error_state")
                raise Exception("Failed in set meal step")

            # Step 5: Click package type dropdown and select Static package
            package_type_dropdown_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[1]/div/div/div/input'
            try:
                print("Clicking package type dropdown...")
                self.take_screenshot("05a_before_package_type")
                
                # Wait for dropdown to be clickable
                dropdown = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, package_type_dropdown_xpath))
                )
                
                # Scroll dropdown into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
                time.sleep(1)
                
                # Click dropdown
                dropdown.click()
                time.sleep(1)
                
                self.take_screenshot("05b_after_dropdown_click")
                
                # Wait for dropdown options to appear
                print("Waiting for dropdown options...")
                WebDriverWait(self.driver, 10).until(
                    lambda driver: any(
                        d.is_displayed() for d in driver.find_elements(By.XPATH, "//ul[contains(@class, 'el-select-dropdown__list')]")
                    )
                )
                
                # Find and click Static package option
                print("Selecting Static package...")
                dropdowns = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'el-select-dropdown__list')]")
                found = False
                
                for dropdown in dropdowns:
                    if dropdown.is_displayed():
                        options = dropdown.find_elements(By.TAG_NAME, "li")
                        for option in options:
                            if "Static" in option.text or "静态" in option.text:
                                # Scroll option into view
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                                time.sleep(0.5)
                                
                                # Try multiple click methods
                                try:
                                    option.click()
                                except:
                                    try:
                                        self.driver.execute_script("arguments[0].click();", option)
                                    except:
                                        ActionChains(self.driver).move_to_element(option).click().perform()
                                
                                print("Selected Static package")
                                found = True
                                break
                        if found:
                            break
                
                if not found:
                    raise Exception("Could not find Static package option")
                
                self.take_screenshot("05c_after_static_selection")
                
                # Wait for selection to be applied
                time.sleep(2)
                
            except Exception as e:
                print(f"Failed to select package type: {str(e)}")
                self.take_screenshot("05d_error_state")
                raise Exception("Failed to select package type")

            # Step 6: Click type dropdown and select first option
            type_dropdown_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[2]/div/div/div/input'
            if not self.click_element(type_dropdown_xpath, "type dropdown"):
                raise Exception("Failed to click type dropdown")
            try:
                print("Selecting first option from type dropdown...")
                WebDriverWait(self.driver, 3).until(lambda driver: any(
                    d.is_displayed() for d in driver.find_elements(By.XPATH, "//ul[contains(@class, 'el-select-dropdown__list')]")
                ))
                dropdowns = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'el-select-dropdown__list')]")
                for dropdown in dropdowns:
                    if dropdown.is_displayed():
                        options = dropdown.find_elements(By.TAG_NAME, "li")
                        if options:
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", options[0])
                            self.driver.execute_script("arguments[0].click();", options[0])
                            print("Selected first option in dropdown")
                        else:
                            raise Exception("No options found in visible dropdown")
                        break
                else:
                    raise Exception("No visible dropdown found")
            except Exception as e:
                print(f"Failed to select first option in type dropdown: {str(e)}")
                self.driver.save_screenshot("type_dropdown_first_option_error.png")
                raise Exception("Failed to select first option in type dropdown")

            # Step 7: Click package name dropdown and select the second option
            package_name_dropdown_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[3]/div/div/div/div[1]/div[1]/input'
            if not self.click_element(package_name_dropdown_xpath, "package name dropdown"):
                raise Exception("Failed to click package name dropdown")
            try:
                print("Selecting second option from package name dropdown...")
                WebDriverWait(self.driver, 3).until(lambda driver: any(
                    d.is_displayed() for d in driver.find_elements(By.XPATH, "//ul[contains(@class, 'el-select-dropdown__list')]")
                ))
                dropdowns = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'el-select-dropdown__list')]")
                for dropdown in dropdowns:
                    if dropdown.is_displayed():
                        options = [opt for opt in dropdown.find_elements(By.TAG_NAME, "li") if opt.is_displayed() and "is-disabled" not in opt.get_attribute("class")]
                        if len(options) >= 2:
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", options[1])
                            self.driver.execute_script("arguments[0].click();", options[1])
                            print("Selected second enabled/visible option in package name dropdown")
                        else:
                            raise Exception("Less than two enabled/visible options found in visible dropdown")
                        break
                else:
                    raise Exception("No visible dropdown found")
            except Exception as e:
                print(f"Failed to select second option in package name dropdown: {str(e)}")
                self.driver.save_screenshot("package_name_dropdown_second_option_error.png")
                raise Exception("Failed to select second option in package name dropdown")

            # Now wait for table row
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr")))

            # Step 8 & 9: Click on number box, clear, and enter 3
            number_box_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[3]/div/div/div/div[2]/div/input'
            new_amount_input_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[2]/div/form/div[6]/div/div/input'
            try:
                print("[DEBUG] Clicking number box, clearing, and entering 3...", flush=True)
                number_box = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, number_box_xpath)))
                number_box.click()
                number_box.clear()
                # Extra clear: send CTRL+A and BACKSPACE to ensure it's empty
                number_box.send_keys(Keys.CONTROL, 'a')
                number_box.send_keys(Keys.BACKSPACE)
                number_box.send_keys("3")
                print("[DEBUG] Entered 3 in number box", flush=True)
                # Now enter 3 in the new amount input
                print("[DEBUG] Entering 3 in new amount input field", flush=True)
                amount_field = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, new_amount_input_xpath)))
                amount_field.clear()
                amount_field.send_keys("3")
                print("[DEBUG] Entered 3 in new amount input field", flush=True)
            except Exception as e:
                print(f"[ERROR] Failed to set number box and amount: {str(e)}", flush=True)
                self.driver.save_screenshot("number_box_or_amount_error.png")
                raise Exception("Failed to set number box and amount")

            # Step 10: Click sure button
            sure_button_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[6]/div/div/div[3]/span/button[2]'
            alternative_sure_button_xpath = "//span/button[contains(., '确定') or contains(., 'Sure') or contains(., '确认')]"
            try:
                print("Clicking sure button...")
                self.take_screenshot("10a_before_click_sure")
                
                # Try main XPath first
                try:
                    sure_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, sure_button_xpath)))
                except Exception:
                    print("Main sure button XPath not found, trying alternative...")
                    sure_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, alternative_sure_button_xpath)))
                
                # Scroll into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sure_button)
                time.sleep(0.5)
                
                self.take_screenshot("10b_after_scroll")
                
                # Try JS click
                try:
                    self.driver.execute_script("arguments[0].click();", sure_button)
                    print("Clicked sure button with JS")
                except Exception as js_e:
                    print(f"JS click failed: {js_e}, trying ActionChains...")
                    try:
                        ActionChains(self.driver).move_to_element(sure_button).click().perform()
                        print("Clicked sure button with ActionChains")
                    except Exception as ac_e:
                        print(f"ActionChains click failed: {ac_e}")
                        raise
                
                self.take_screenshot("10c_after_click")
                
                # Wait for any loading indicators to disappear
                try:
                    WebDriverWait(self.driver, 10).until_not(
                        EC.presence_of_element_located((By.CLASS_NAME, "el-loading-mask"))
                    )
                except:
                    print("No loading mask found or already disappeared")
                
                self.take_screenshot("10d_after_loading_mask")
                
                # Wait for the dialog to close
                try:
                    WebDriverWait(self.driver, 10).until_not(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'el-dialog')]"))
                    )
                except:
                    print("No dialog found or already closed")
                
                self.take_screenshot("10e_after_dialog_close")
                
                # Wait for the list to update and verify the item appears
                print("Waiting for list to update...")
                try:
                    # Wait for table to be present
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
                    )
                    
                    # Wait for the new item to appear in the list
                    WebDriverWait(self.driver, 10).until(
                        lambda driver: len(driver.find_elements(By.XPATH, "//table//tbody/tr")) > 0
                    )
                    
                    # Take screenshot of the list
                    self.take_screenshot("10f_list_updated")
                    
                    # Verify the item is in the list
                    rows = self.driver.find_elements(By.XPATH, "//table//tbody/tr")
                    if len(rows) > 0:
                        print(f"Found {len(rows)} items in the list")
                    else:
                        print("Warning: No items found in the list")
                        self.take_screenshot("10g_no_items_in_list")
                        
                except Exception as e:
                    print(f"Failed to verify list update: {str(e)}")
                    self.take_screenshot("10h_list_verification_failed")
                
                # Additional wait time after clicking
                print("Waiting for page to stabilize after clicking sure button...")
                time.sleep(5)
                
                self.take_screenshot("10i_final_state")
                
            except Exception as e:
                print(f"Failed to click sure button: {str(e)}")
                self.take_screenshot("10j_error_state")
                raise Exception("Failed to click sure button")

            # Step 11: Click payment button
            payment_button_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[4]/div[2]/div[1]/div/div[3]/table/tbody/tr[1]/td[19]/div/div/div/button[1]'
            try:
                print("Clicking payment button...")
                # Take screenshot before clicking payment button
                self.take_screenshot("11a_before_click_payment")
                
                payment_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, payment_button_xpath)))
                self.driver.execute_script("arguments[0].click();", payment_button)
                print("Clicked payment button")
                
                # Take screenshot after clicking payment button
                self.take_screenshot("11b_after_click_payment")
                
                time.sleep(2)
            except Exception as e:
                print(f"Failed to click payment button: {str(e)}")
                self.take_screenshot("11c_error_state")
                raise Exception("Failed to click payment button")

            # Step 12: Handle popup and click sure button
            popup_sure_button_xpath = '//*[@id="app"]/div/div/section/div/div[2]/div[4]/div[3]/div/div/div[3]/span/button[2]'
            try:
                print("Clicking popup sure button...")
                popup_sure_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, popup_sure_button_xpath)))
                self.driver.execute_script("arguments[0].click();", popup_sure_button)
                print("Clicked popup sure button")
                time.sleep(2)
            except Exception as e:
                print(f"Failed to click popup sure button: {str(e)}")
                self.driver.save_screenshot("popup_sure_button_error.png")
                raise Exception("Failed to click popup sure button")

            # Step 13: Click static package tab
            try:
                print("Clicking static package tab...")
                self.take_screenshot("13a_before_static_tab")
                
                # Wait for page to be ready after previous operations
                time.sleep(3)
                
                # Multiple XPath options for the tab
                static_tab_xpaths = [
                    '//*[@id="tab-staticPackage"]/font/font',
                    '//*[@id="tab-staticPackage"]',
                    '//div[contains(@id, "tab-staticPackage")]',
                    '//div[@role="tab" and contains(text(), "Static")]',
                    '//div[@role="tab" and contains(text(), "静态")]'
                ]
                
                tab_clicked = False
                for xpath in static_tab_xpaths:
                    try:
                        print(f"Trying XPath: {xpath}")
                        
                        # Wait for tab to be present and clickable
                        tab_element = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        
                        # Scroll tab into view
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab_element)
                        time.sleep(1)
                        
                        # Add visual highlight
                        self.driver.execute_script("""
                            arguments[0].style.border = '3px solid red';
                            arguments[0].style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
                        """, tab_element)
                        
                        self.take_screenshot(f"13b_tab_found_{xpath.split('/')[-1]}")
                        
                        # Try multiple click methods
                        try:
                            tab_element.click()
                            print("Clicked tab with regular click")
                        except:
                            try:
                                self.driver.execute_script("arguments[0].click();", tab_element)
                                print("Clicked tab with JS click")
                            except:
                                ActionChains(self.driver).move_to_element(tab_element).click().perform()
                                print("Clicked tab with ActionChains")
                        
                        # Verify tab is active
                        time.sleep(2)
                        if "is-active" in tab_element.get_attribute("class") or "active" in tab_element.get_attribute("class"):
                            print("Tab is now active")
                            tab_clicked = True
                            break
                        else:
                            print("Tab click may not have worked, checking content...")
                            # Check if the static package content is visible
                            try:
                                WebDriverWait(self.driver, 3).until(
                                    EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
                                )
                                print("Static package content is visible")
                                tab_clicked = True
                                break
                            except:
                                print("Static package content not visible yet")
                        
                    except Exception as e:
                        print(f"Failed with XPath {xpath}: {str(e)}")
                        continue
                
                if not tab_clicked:
                    raise Exception("Failed to click static package tab with all XPaths")
                
                self.take_screenshot("13c_after_tab_click")
                
                # Wait for tab content to load
                print("Waiting for static package tab content to load...")
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//table//tbody"))
                )
                
                time.sleep(3)  # Additional wait for content to stabilize
                self.take_screenshot("13d_tab_content_loaded")
                
            except Exception as e:
                print(f"Failed to click static package tab: {str(e)}")
                self.take_screenshot("13e_tab_error")
                raise Exception("Failed to click static package tab")

            # Step 14: Click Closure button
            try:
                print("Clicking Closure button...")
                self.take_screenshot("14a_before_closure")
                
                # Multiple XPaths for the closure button
                closure_button_xpaths = [
                    '//*[@id="app"]/div/div/section/div/div[2]/div[4]/div[2]/div[1]/div/div[3]/table/tbody/tr[1]/td[8]/div/div/div/div/button[4]/span/font/font',
                    '//table//tbody/tr[1]//button[contains(@class, "el-button") and contains(., "Closure")]',
                    '//table//tbody/tr[1]//button[contains(@class, "el-button") and contains(., "关闭")]',
                    '//table//tbody/tr[1]//button[4]',
                    '//table//tbody/tr[1]/td[8]//button[contains(., "Closure")]',
                    '//button[contains(text(), "Closure") or contains(text(), "关闭")]'
                ]
                
                closure_clicked = False
                for xpath in closure_button_xpaths:
                    try:
                        print(f"Trying closure XPath: {xpath}")
                        
                        # Wait for button to be clickable
                        closure_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        
                        # Scroll button into view
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", closure_button)
                        time.sleep(1)
                        
                        # Add visual highlight
                        self.driver.execute_script("""
                            arguments[0].style.border = '3px solid green';
                            arguments[0].style.backgroundColor = 'rgba(0, 255, 0, 0.3)';
                        """, closure_button)
                        
                        self.take_screenshot(f"14b_closure_found_{xpath.split('/')[-1]}")
                        
                        # Try multiple click methods
                        try:
                            closure_button.click()
                            print("Clicked closure button with regular click")
                        except:
                            try:
                                self.driver.execute_script("arguments[0].click();", closure_button)
                                print("Clicked closure button with JS click")
                            except:
                                ActionChains(self.driver).move_to_element(closure_button).click().perform()
                                print("Clicked closure button with ActionChains")
                        
                        closure_clicked = True
                        break
                        
                    except Exception as e:
                        print(f"Failed with closure XPath {xpath}: {str(e)}")
                        continue
                
                if not closure_clicked:
                    raise Exception("Failed to click Closure button with all XPaths")
                
                self.take_screenshot("14c_after_closure_click")
                
                # Wait for any confirmation dialog or page update
                time.sleep(3)
                self.take_screenshot("14d_after_closure_wait")
                
            except Exception as e:
                print(f"Failed to click Closure button: {str(e)}")
                self.take_screenshot("14e_closure_error")
                raise Exception("Failed to click Closure button")

            print("Test completed successfully!")
            self.take_screenshot("15_final_success")

            # Refresh the page and keep browser open
            self.driver.refresh()
            print("Page refreshed. Browser will remain open. Press Enter in the terminal to close it.")
            input("Press Enter to exit and close the browser...")

        except Exception as e:
            print(f"Test failed: {str(e)}")
            self.take_screenshot("final_error_state")
            raise

if __name__ == '__main__':
    unittest.main(verbosity=2)
