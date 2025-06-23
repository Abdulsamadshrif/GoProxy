"""
Selenium Test Automation for Payment System
This script automates the process of:
1. Login with cookies
2. Test wallet payment with balance
3. Test wallet payment without balance
4. Test Google Pay payment
5. Test PayPal payment
"""

# ===== Imports =====
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pytest
import os
import time
from datetime import datetime
import logging

# ===== Global Configuration =====
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)  # Increased timeout to 20 seconds

# Maximize the browser window to ensure full visibility
driver.maximize_window()

# ===== Utility Functions =====
def create_report_dir():
    """Creates a timestamped directory for test reports"""
    report_dir = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_dir = os.path.join(report_dir, f"Target_proxies_payment_{timestamp}")
    os.makedirs(test_dir)
    return test_dir

def take_screenshot(driver, step_name, report_dir):
    """Takes and saves a screenshot with the given step name"""
    screenshot_path = os.path.join(report_dir, f"{step_name}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

def highlight_and_wait(driver, element, wait_time=1):
    """Highlights an element with a red border and waits"""
    driver.execute_script("arguments[0].style.border='3px solid red'", element)
    time.sleep(wait_time)

def interact_with_element(driver, element, action, step_name, report_dir, wait_time=1, **kwargs):
    """Handles element interaction with screenshots and highlighting"""
    try:
        driver.execute_script("arguments[0].style.border='3px solid red'", element)
        time.sleep(1)
        
        if action == "click":
            element.click()
        elif action == "send_keys":
            element.send_keys(kwargs.get('keys', ''))
        elif action == "clear":
            element.clear()
        elif action == "submit":
            element.submit()
        
        time.sleep(wait_time)
        take_screenshot(driver, step_name, report_dir)
        
    except Exception as e:
        raise Exception(f"Failed to {action} element: {str(e)}")

def wait_for_page_load(driver, wait):
    """Wait for the page to load completely"""
    try:
        wait.until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
        print("Page loaded successfully")
    except TimeoutException:
        print("Page load timeout")
        raise

# ===== Test Step Functions =====
def add_auth_cookies(driver, account_type="with_balance", report_dir=None):
    """Add authentication cookies based on account type"""
    try:
        print("\n=== Starting authentication with cookies ===")
        # First navigate to the domain to set cookies
        driver.get("https://test-goproxy.xiaoxitech.com")
        wait_for_page_load(driver, wait)
        
        # Define cookies based on account type
        if account_type == "with_balance":
            cookies = {
                "Admin_Token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHQiOiJ7XCJhY3RpdmVcIjp0cnVlLFwibG9naW5fZmxhZ1wiOlwiMjFmYmI2YTFjMGNjMjVjNWEzNjkzMDgyMTNiM2QwOTZcIn0iLCJ1c2VyX25hbWUiOiJhbWFuZGExQGdldG5hZGEuY29tIiwic2NvcGUiOlsiYWxsIl0sImV4cCI6MTc1MTk0MjY5NiwidXNlcklkIjoiMTkyNDM3NTE4Nzc1OTk1NTk2OCIsImp0aSI6ImNmMjE5MTI0LWJkZDQtNDg1Yy05MzQ0LTRlYjNjMWRmY2FkMSIsImNsaWVudF9pZCI6ImdvX3Byb3h5In0.MLf8KO1iJ7Te-H0NcB6Y74KYY1r1uEGrEWF6IfHt7YHtp1mc21L31lO-f61QHbajDYp5S36YndPl3CpvjMwOC_408jjIIINqI55HSxdmQRFWAbzn_3ACdetqWDc0zQ4ecWNb6xSpPwzG9Z1q9cR-vQxAYHCZec54LHo3osIOGJ04-fXy0tdTkocAmxyWJae2IGhQJVtkTBLxa8sQbuiPfwIlkue0Z4S8FB_izwcPblUoCqg1mqgr4N2efqQJAQ8ZpaPiNSoxIrFm5zpEWakRC02d0OrOVtokwq4zuqvXMA9txFtkJedJ9H-STRTuShFhfv4rT-ZneoQhw-K14aQF5g"
            }
        else:  # without_balance
            cookies = {
                "Admin_Token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHQiOiJ7XCJhY3RpdmVcIjp0cnVlLFwibG9naW5fZmxhZ1wiOlwiY2RlNDQ2OTIyZDBmMjRkZTMyMGEyNGYyZWU2OTA0MDhcIn0iLCJ1c2VyX25hbWUiOiJhbWFuZGEyQGdldG5hZGEuY29tIiwic2NvcGUiOlsiYWxsIl0sImV4cCI6MTc1MTk0MjgyMywidXNlcklkIjoiMTkyNDY1ODAxNjExNjkzMjYwOCIsImp0aSI6ImJhYjc1MTUyLWYzYTMtNGE2Yy04M2Q4LWViYmM0ZGQ4ZjI5NiIsImNsaWVudF9pZCI6ImdvX3Byb3h5In0.sMZvSRLstX0PCJjsBbYK6R5nQlHyjGmpo1nskuVtcx_D-7TMdM2AWRk5Bxy0Y8dZVm23rvrjVFZc1Mpsig9t73dvDqsyB1iGfaxVX_zk7EPyqC3umigD0OSdaoyaidHvzmzPvlFQvXMw9rPeUFQGOqwxY8vAc1zJD2O4a0Wmeya7_mvM5XGGyxIgUUfD86J-ldXJoS2B5nL9GaiU7KQWRKB4t6ZXKXHodvtgh5gLs1JpnS21f34RNNLeX5NliO_UV9QD5Jh_g1KxA-WQ_jZeNKYMc_wGkvypyszd1kYFH0mPeSu2Pm1_Evxx7loQV88OXbB1VXxrVYVn_UFBXip9qA"
            }
        
        # Add cookies
        for name, value in cookies.items():
            driver.add_cookie({'name': name, 'value': value})
        print(f"Added authentication cookies for {account_type} account")
            
    except Exception as e:
        print(f"Failed to add cookies: {str(e)}")
        if report_dir:
            take_screenshot(driver, "error_cookies", report_dir)
        raise

def setup_prerequisites(driver, wait, report_dir):
    """Setup prerequisites before running payment tests"""
    print("\n=== Setting up prerequisites ===")
    
    # Step 1: Navigate to buy proxy page
    print("\n--- Step 1: Navigating to buy proxy page ---")
    driver.get("https://test-goproxy.xiaoxitech.com/dashboard/buyproxy?mealType=7")
    wait_for_page_load(driver, wait)
    time.sleep(3)
    
    # Step 2: Find and click search bar
    print("\n--- Step 2: Finding and clicking search bar ---")
    try:
        search_bar = wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/section/section/main/div/div[1]/div[2]/main/div/div[2]/div[1]/div[2]/div/input"))
        )
        search_bar.clear()
        search_bar.send_keys("Daegu, South Korea")
    except Exception as e:
        print(f"ERROR: Failed to find or interact with search bar: {str(e)}")
        take_screenshot(driver, "error_search_bar", report_dir)
        raise
    
    # Step 3: Click search button
    print("\n--- Step 3: Clicking search button ---")
    try:
        search_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/section/section/main/div/div[1]/div[2]/main/div/div[2]/div[1]/div[2]/button"))
        )
        search_button.click()
        time.sleep(2)  # Wait for search results
    except Exception as e:
        print(f"ERROR: Failed to click search button: {str(e)}")
        take_screenshot(driver, "error_search_button", report_dir)
        raise
    
    # Step 4: Wait for and find Canberra result
    print("\n--- Step 4: Finding Canberra result ---")
    try:
        canberra_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/section/section/main/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/div/div"))
        )
        print("Found Canberra, Australia element")
    except Exception as e:
        print(f"ERROR: Failed to find Canberra element: {str(e)}")
        take_screenshot(driver, "error_canberra", report_dir)
        raise
    
    # Step 5: Hover over the element
    print("\n--- Step 5: Hovering over element ---")
    try:
        hover_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/section/section/main/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[2]/div/div"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(hover_element).perform()
        time.sleep(1)
    except Exception as e:
        print(f"ERROR: Failed to hover: {str(e)}")
        take_screenshot(driver, "error_hover", report_dir)
        raise
    
    # Step 6: Set quantity directly in input field
    print("\n--- Step 6: Setting quantity in input field ---")
    try:
        # Wait for the input field to be present and visible
        quantity_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.el-input-number input.el-input__inner"))
        )
        print("Found quantity input")
        time.sleep(1)
        # Clear and type 3
        quantity_input.clear()
        quantity_input.send_keys("3")
        time.sleep(2)  # Wait a second after typing
        # Verify the value was set correctly
        value = quantity_input.get_attribute("value")
        print(f"Current input value: {value}")
        if value == "03":
            print("Successfully set quantity to 3")
        else:
            raise Exception(f"Failed to set quantity value. Current value: {value}")
    except Exception as e:
        print(f"ERROR: Failed to set quantity: {str(e)}")
        take_screenshot(driver, "error_quantity_set", report_dir)
        raise
    
    # Step 7: Click Buy Now button
    print("\n--- Step 7: Clicking Buy Now button ---")
    try:
        buy_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='account']/div[2]/div/div[4]/button"))
        )
        print("Found buy button, attempting to hover...")
        
        # Hover over the button first
        actions = ActionChains(driver)
        actions.move_to_element(buy_button).perform()
        time.sleep(2)  # Wait after hover
        
        # Wait for button to be clickable
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='account']/div[2]/div/div[4]/button")))
        print("Buy button is now clickable")
        
        # Scroll into view and click
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", buy_button)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", buy_button)
        time.sleep(2)
    except Exception as e:
        print(f"ERROR: Failed to click Buy Now button: {str(e)}")
        take_screenshot(driver, "error_buy_button", report_dir)
        raise
    
    # Wait for navigation to payment page
    wait.until(
        lambda driver: "dashboard/pay/staticResidence" in driver.current_url
    )
    print("Successfully navigated to payment page")
    time.sleep(2)

def login(report_dir):
    """Handles the login process"""
    try:
        print("\n=== Starting login process ===")
        driver.get("https://sso.xiaoxitech.com/login?project=lwlu63w1&cb=https%3A%2F%2Ftest-admin-ipipgo.cd.xiaoxigroup.net%2Fapp-manager%2F")
        print("Navigated to login page")
        
        # Step 1: Click initial button
        try:
            print("\n--- Step 1: Clicking initial button ---")
            initial_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/form/div[2]/div/div/button/span')))
            print("Found initial button")
            initial_button.click()
        except Exception as e:
            print(f"ERROR: Failed to click initial button: {str(e)}")
            raise
        
        # Step 2: Wait for login form
        try:
            print("\n--- Step 2: Waiting for login form ---")
            login_form = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/form/div[4]/div/button/span')))
            print("Login form appeared")
        except Exception as e:
            print(f"ERROR: Failed to find login form: {str(e)}")
            raise
        
        # Step 3: Enter username
        try:
            print("\n--- Step 3: Entering username ---")
            username_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/form/div[1]/div/div[1]/input')
            print("Found username input")
            username_input.send_keys("abdullahahmad")
        except Exception as e:
            print(f"ERROR: Failed to enter username: {str(e)}")
            raise
        
        # Step 4: Enter password
        try:
            print("\n--- Step 4: Entering password ---")
            password_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/form/div[2]/div/div/input')
            print("Found password input")
            password_input.send_keys("Ahmad21@21@")
        except Exception as e:
            print(f"ERROR: Failed to enter password: {str(e)}")
            raise
        
        # Step 5: Wait for manual CAPTCHA
        print("\n--- Step 5: Waiting for manual CAPTCHA and login ---")
        print("Please complete the CAPTCHA and click the login button manually")
        input("Press Enter after you have completed the CAPTCHA and clicked login...")
        
        # Step 6: Verify login success
        try:
            print("\n--- Step 6: Verifying login success ---")
            wait.until(EC.url_contains("test-admin-ipipgo.cd.xiaoxigroup.net/app-manager"))
            print("Login successful")
        except Exception as e:
            print(f"ERROR: Failed to verify login: {str(e)}")
            raise
            
    except Exception as e:
        print(f"\n=== Login failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise

def close_package(report_dir):
    """Closes the first package in the admin panel"""
    try:
        print("\n=== Starting package closure process ===")
        # First navigate to the correct admin URL
        print("\n--- Step 1: Navigating to admin panel ---")
        driver.get("https://test-admin-goproxy.xiaoxitech.com")
        wait_for_page_load(driver, wait)
        time.sleep(2)  # Wait for any redirects
        
        # Now navigate to customer details page
        print("\n--- Step 2: Navigating to customer details ---")
        driver.get("https://test-admin-goproxy.xiaoxitech.com/customer/userList/customerDetails?id=871&brand=goproxy")
        wait_for_page_load(driver, wait)
        time.sleep(2)  # Wait for page to fully load
        take_screenshot(driver, "5-1", report_dir)
        
        # Click on Static Package tab
        try:
            print("\n--- Step 3: Clicking Static Package tab ---")
            time.sleep(2)  # Wait for 2 seconds before clicking
            static_package_tab = wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/section/div/div[2]/div[3]/div[1]/div/div/div/div[8]"))
            )
            static_package_tab.click()
            time.sleep(2)
            take_screenshot(driver, "5-2", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click Static Package tab: {str(e)}")
            raise
        
        # Click Closure button
        try:
            print("\n--- Step 4: Clicking Closure button ---")
            closure_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/section/div/div[2]/div[4]/div[2]/div[1]/div/div[3]/table/tbody/tr[1]/td[9]/div/div/div/div/button[4]"))
            )
            closure_button.click()
            time.sleep(2)
            take_screenshot(driver, "5-3", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click Closure button: {str(e)}")
            raise
        
        # Verify success message appears
        try:
            print("\n--- Step 5: Verifying success message appears ---")
            # Wait for success message to appear (it only shows for 1.5 seconds)
            success_message = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.el-message.el-message--success"))
            )
            # Immediately take screenshot and get text since message disappears quickly
            take_screenshot(driver, "5-4", report_dir)
            success_text = success_message.text
            print(f"Found success message: {success_text}")
            print("Package closure success message verified")
                
        except Exception as e:
            print(f"ERROR: Failed to verify success message: {str(e)}")
            # Try to take screenshot even if verification fails
            take_screenshot(driver, "5-4", report_dir)
            raise
            
    except Exception as e:
        print(f"\n=== Package closure failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise

def test_wallet_payment_with_balance(driver, report_dir):
    """Test case for wallet payment with sufficient balance"""
    try:
        print("\n=== Starting wallet payment with balance test ===")
        # Add authentication cookies
        add_auth_cookies(driver, "with_balance", report_dir)
        
        # Setup prerequisites
        setup_prerequisites(driver, wait, report_dir)
        
        # Navigate to the payment page
        driver.get("https://test-goproxy.xiaoxitech.com/dashboard/pay/staticResidence?type=TAG&mealId=1856519604361363456&mealType=7")
        
        # Wait for page to load completely
        print("Waiting for page to load completely...")
        wait_for_page_load(driver, wait)
        time.sleep(3)  # Additional wait to ensure dynamic content loads
        take_screenshot(driver, "1-1", report_dir)
        
        # Select Wallet payment method
        try:
            print("\n--- Step 1: Selecting Wallet Payment Method ---")
            # Wait for payment methods to be visible and clickable
            print("Waiting for payment methods to be visible...")
            
            # Try multiple selectors to find the wallet payment method
            selectors = [
                "div[data-v-7d4d3948].pay-title.wallet-pay-title",  # Exact class and data attribute
                "div.pay-title.wallet-pay-title",  # Just the classes
                "div[data-v-7d4d3948] span:contains('Wallet')",  # Data attribute with Wallet text
                "//div[contains(@class, 'wallet-pay-title')]//span[text()='Wallet']"  # XPath with exact text
            ]
            
            wallet_option = None
            for selector in selectors:
                try:
                    print(f"Trying selector: {selector}")
                    if selector.startswith("//"):
                        # XPath selector
                        elements = driver.find_elements(By.XPATH, selector)
                    else:
                        # CSS selector
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements:
                        wallet_option = elements[0]
                        print(f"Found wallet option with selector: {selector}")
                        break
                except Exception as e:
                    print(f"Selector {selector} failed: {str(e)}")
                    continue
            
            if wallet_option:
                # Scroll the wallet option into view
                print("Scrolling wallet option into view...")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", wallet_option)
                time.sleep(1)  # Wait for scroll to complete
                
                # Wait for the wallet option to be clickable
                wait.until(EC.element_to_be_clickable(wallet_option))
                print("Wallet option is clickable")
                
                # Try to click using JavaScript
                try:
                    print("Attempting to click using JavaScript")
                    driver.execute_script("arguments[0].click();", wallet_option)
                    print("Clicked wallet option using JavaScript")
                except Exception as e:
                    print(f"JavaScript click failed: {str(e)}")
                    # Fallback to regular click
                    wallet_option.click()
                    print("Clicked wallet option using regular click")
                
                take_screenshot(driver, "1-2", report_dir)
            else:
                raise Exception("Could not find wallet payment method with any selector")
                
        except Exception as e:
            print(f"ERROR: Failed to select wallet payment: {str(e)}")
            take_screenshot(driver, "error_wallet_selection", report_dir)
            raise
        
        # Debug: Print all visible buttons and their HTML after wallet selection
        print("\n--- Debug: Printing all visible buttons after wallet selection ---")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            print(f"Button text: {button.text}, HTML: {button.get_attribute('outerHTML')}")
        
        # Click Payment button
        try:
            print("\n--- Step 2: Clicking Payment Button ---")
            # Wait for payment button to be clickable
            time.sleep(2)  # Additional wait after selecting payment method
            
            # Use the exact selector from the debug output
            payment_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.el-button.buy-btn.el-button--primary"))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", payment_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", payment_button)
            take_screenshot(driver, "1-3", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click payment button: {str(e)}")
            take_screenshot(driver, "error_payment_button", report_dir)
            raise
        
        # Verify payment success by checking redirect
        try:
            print("\n--- Step 3: Verifying Payment Success Redirect ---")
            # Wait for redirect to payment success page
            wait.until(
                lambda driver: "payment-success" in driver.current_url and "orderNo" in driver.current_url
            )
            print(f"Successfully redirected to: {driver.current_url}")
            take_screenshot(driver, "1-4", report_dir)
            return True
        except Exception as e:
            print(f"Failed to verify payment success redirect: {str(e)}")
            take_screenshot(driver, "error_payment_success", report_dir)
            return False
            
    except Exception as e:
        print(f"\n=== Test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise

def test_wallet_payment_without_balance(driver, report_dir):
    """Test case for wallet payment with zero balance"""
    try:
        print("\n=== Starting wallet payment without balance test ===")
        # Add authentication cookies
        add_auth_cookies(driver, "without_balance", report_dir)
        
        # Setup prerequisites
        setup_prerequisites(driver, wait, report_dir)
        
        # Navigate to the payment page
        driver.get("https://test-goproxy.xiaoxitech.com/dashboard/pay/staticResidence?type=TAG&mealId=1856519604361363456&mealType=7")
        wait_for_page_load(driver, wait)
        take_screenshot(driver, "2-1", report_dir)
        
        # Select Wallet payment method
        try:
            print("\n--- Step 1: Selecting Wallet Payment Method ---")
            # Try multiple selectors to find the wallet payment method
            selectors = [
                "div[data-v-7d4d3948].pay-title.wallet-pay-title",  # Exact class and data attribute
                "div.pay-title.wallet-pay-title",  # Just the classes
                "div[data-v-7d4d3948] span:contains('Wallet')",  # Data attribute with Wallet text
                "//div[contains(@class, 'wallet-pay-title')]//span[text()='Wallet']"  # XPath with exact text
            ]
            
            wallet_option = None
            for selector in selectors:
                try:
                    print(f"Trying selector: {selector}")
                    if selector.startswith("//"):
                        # XPath selector
                        elements = driver.find_elements(By.XPATH, selector)
                    else:
                        # CSS selector
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements:
                        wallet_option = elements[0]
                        print(f"Found wallet option with selector: {selector}")
                        break
                except Exception as e:
                    print(f"Selector {selector} failed: {str(e)}")
                    continue
            
            if wallet_option:
                # Scroll the wallet option into view
                print("Scrolling wallet option into view...")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", wallet_option)
                time.sleep(1)  # Wait for scroll to complete
                
                # Wait for the wallet option to be clickable
                wait.until(EC.element_to_be_clickable(wallet_option))
                print("Wallet option is clickable")
                
                # Try to click using JavaScript
                try:
                    print("Attempting to click using JavaScript")
                    driver.execute_script("arguments[0].click();", wallet_option)
                    print("Clicked wallet option using JavaScript")
                except Exception as e:
                    print(f"JavaScript click failed: {str(e)}")
                    # Fallback to regular click
                    wallet_option.click()
                    print("Clicked wallet option using regular click")
                
                take_screenshot(driver, "2-2", report_dir)
            else:
                raise Exception("Could not find wallet payment method with any selector")
                
        except Exception as e:
            print(f"ERROR: Failed to select wallet payment: {str(e)}")
            take_screenshot(driver, "error_wallet_selection", report_dir)
            raise
        
        # Click Payment button
        try:
            print("\n--- Step 2: Clicking Payment Button ---")
            # Wait for payment button to be clickable
            time.sleep(2)  # Additional wait after selecting payment method
            
            # Use the exact selector from the debug output
            payment_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.el-button.buy-btn.el-button--primary"))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", payment_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", payment_button)
            take_screenshot(driver, "2-3", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click payment button: {str(e)}")
            take_screenshot(driver, "error_payment_button", report_dir)
            raise
        
        # Verify error dialog
        try:
            print("\n--- Step 3: Verifying Error Dialog ---")
            # Wait for error dialog to appear
            error_dialog = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.el-dialog.el-dialog--center"))
            )
            print(f"Found error dialog: {error_dialog.text}")
            take_screenshot(driver, "2-4", report_dir)
            
            # Verify the warning image is present
            warning_img = error_dialog.find_element(By.CSS_SELECTOR, "img[alt='GoProxy']")
            if warning_img:
                print("Warning image found in dialog")
            
            return True
        except Exception as e:
            print(f"Failed to verify error dialog: {str(e)}")
            take_screenshot(driver, "error_verification", report_dir)
            return False
            
    except Exception as e:
        print(f"\n=== Test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise

def test_google_pay_payment(driver, report_dir):
    """Test case for Google Pay payment"""
    try:
        print("\n=== Starting Google Pay payment test ===")
        # Add authentication cookies
        add_auth_cookies(driver, "without_balance", report_dir)
        
        # Setup prerequisites
        setup_prerequisites(driver, wait, report_dir)
        
        # Navigate to the payment page
        driver.get("https://test-goproxy.xiaoxitech.com/dashboard/pay/staticResidence?type=TAG&mealId=1856519604361363456&mealType=7")
        wait_for_page_load(driver, wait)
        take_screenshot(driver, "3-1", report_dir)
        
        # Debug: Print all payment method elements
        print("\n--- Debug: Printing all payment method elements ---")
        payment_methods = driver.find_elements(By.CSS_SELECTOR, "div[data-v-199ea5d0].pay-info")
        for method in payment_methods:
            print(f"Payment method HTML: {method.get_attribute('outerHTML')}")
            print(f"Is active: {method.get_attribute('class')}")
        
        # Select Google Pay payment method
        try:
            print("\n--- Step 1: Selecting Google Pay Payment Method ---")
            # Wait for payment methods to be visible
            print("Waiting for payment methods to be visible...")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-v-199ea5d0].pay-info")))
            time.sleep(2)  # Additional wait to ensure all methods are loaded
            
            # Find all payment method elements
            payment_methods = driver.find_elements(By.CSS_SELECTOR, "div[data-v-199ea5d0].pay-info")
            print(f"Found {len(payment_methods)} payment methods")
            
            # Find the Google Pay option
            gpay_option = None
            for method in payment_methods:
                html = method.get_attribute('outerHTML')
                print(f"Checking payment method: {html}")
                if "Google Pay" in html:
                    gpay_option = method
                    print("Found Google Pay option")
                    break
            
            if gpay_option:
                # Scroll the Google Pay option into view
                print("Scrolling Google Pay option into view...")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", gpay_option)
                time.sleep(1)  # Wait for scroll to complete
                
                # Wait for the Google Pay option to be clickable
                wait.until(EC.element_to_be_clickable(gpay_option))
                print("Google Pay option is clickable")
                
                # Try to click using JavaScript
                try:
                    print("Attempting to click using JavaScript")
                    driver.execute_script("arguments[0].click();", gpay_option)
                    print("Clicked Google Pay option using JavaScript")
                except Exception as e:
                    print(f"JavaScript click failed: {str(e)}")
                    # Fallback to regular click
                    gpay_option.click()
                    print("Clicked Google Pay option using regular click")
                
                take_screenshot(driver, "3-2", report_dir)
            else:
                raise Exception("Could not find Google Pay payment method")
                
        except Exception as e:
            print(f"ERROR: Failed to select Google Pay: {str(e)}")
            take_screenshot(driver, "error_gpay_selection", report_dir)
            raise
        
        # Click Payment button
        try:
            print("\n--- Step 2: Clicking Payment Button ---")
            # Wait for payment button to be clickable
            time.sleep(2)  # Additional wait after selecting payment method
            
            # Use the exact selector from the debug output
            payment_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.el-button.buy-btn.el-button--primary"))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", payment_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", payment_button)
            take_screenshot(driver, "3-3", report_dir)
            
            # Add explicit wait for popup to appear
            print("Waiting for Google Pay popup to appear...")
            time.sleep(3)
        except Exception as e:
            print(f"ERROR: Failed to click payment button: {str(e)}")
            take_screenshot(driver, "error_payment_button", report_dir)
            raise
        
        # Verify Google Pay popup
        try:
            print("\n--- Step 3: Verifying Google Pay Popup ---")
            # Wait for Google Pay dialog to appear
            gpay_dialog = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.el-dialog[aria-label='dialog']"))
            )
            print("Found Google Pay dialog")
            
            # Verify the dialog header and close button
            dialog_header = gpay_dialog.find_element(By.CSS_SELECTOR, "div.el-dialog__header")
            close_button = dialog_header.find_element(By.CSS_SELECTOR, "button.el-dialog__headerbtn")
            if close_button:
                print("Found close button in dialog")
            
            # Verify the Google Pay iframe
            gpay_iframe = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[importance='high']"))
            )
            if gpay_iframe:
                print("Found Google Pay iframe")
            
            take_screenshot(driver, "3-4", report_dir)
            return True
        except Exception as e:
            print(f"Failed to verify Google Pay popup: {str(e)}")
            take_screenshot(driver, "error_gpay_popup", report_dir)
            return False
            
    except Exception as e:
        print(f"\n=== Test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise

def test_paypal_payment(driver, report_dir):
    """Test case for PayPal payment"""
    try:
        print("\n=== Starting PayPal payment test ===")
        # Add authentication cookies
        add_auth_cookies(driver, "without_balance", report_dir)
        
        # Navigate to the payment page
        driver.get("https://test-goproxy.xiaoxitech.com/dashboard/pay/dynamicResidence?mealId=1827952916573487105&mealType=6")
        # Wait for page to load completely
        print("Waiting for page to load completely...")
        wait_for_page_load(driver, wait)
        time.sleep(3)  # Additional wait to ensure dynamic content loads
        take_screenshot(driver, "4-1", report_dir)
        
        # Select PayPal payment method
        try:
            print("\n--- Step 1: Selecting PayPal Payment Method ---")
            # Try multiple selectors to find the PayPal payment method
            selectors = [
                "div[data-v-199ea5d0].pay-info.active",  # Exact active payment info div
                "div[data-v-199ea5d0].pay-title .name.mark",  # The name div containing PayPal text
                "//div[contains(@class, 'pay-info') and contains(@class, 'active')]//div[text()='PayPal']",  # XPath with exact text
                "//div[contains(@class, 'pay-info')]//img[@alt='PayPal']/ancestor::div[contains(@class, 'pay-info')]"  # XPath using the image and finding parent
            ]
            
            paypal_option = None
            for selector in selectors:
                try:
                    print(f"Trying selector: {selector}")
                    if selector.startswith("//"):
                        # XPath selector
                        elements = driver.find_elements(By.XPATH, selector)
                    else:
                        # CSS selector
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements:
                        paypal_option = elements[0]
                        print(f"Found PayPal option with selector: {selector}")
                        break
                except Exception as e:
                    print(f"Selector {selector} failed: {str(e)}")
                    continue
            
            if paypal_option:
                # Scroll the PayPal option into view
                print("Scrolling PayPal option into view...")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", paypal_option)
                time.sleep(1)  # Wait for scroll to complete
                
                # Wait for the PayPal option to be clickable
                wait.until(EC.element_to_be_clickable(paypal_option))
                print("PayPal option is clickable")
                
                # Try to click using JavaScript
                try:
                    print("Attempting to click using JavaScript")
                    driver.execute_script("arguments[0].click();", paypal_option)
                    print("Clicked PayPal option using JavaScript")
                except Exception as e:
                    print(f"JavaScript click failed: {str(e)}")
                    # Fallback to regular click
                    paypal_option.click()
                    print("Clicked PayPal option using regular click")
                
                take_screenshot(driver, "4-2", report_dir)
            else:
                raise Exception("Could not find PayPal payment method with any selector")
                
        except Exception as e:
            print(f"ERROR: Failed to select PayPal: {str(e)}")
            take_screenshot(driver, "error_paypal_selection", report_dir)
            raise
        
        # Click Payment button
        try:
            print("\n--- Step 2: Clicking Payment Button ---")
            # Wait for payment button to be clickable
            time.sleep(2)  # Additional wait after selecting payment method
            
            # Use the exact selector from the debug output
            payment_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.el-button.buy-btn.el-button--primary"))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", payment_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", payment_button)
            take_screenshot(driver, "4-3", report_dir)
        except Exception as e:
            print(f"ERROR: Failed to click payment button: {str(e)}")
            take_screenshot(driver, "error_payment_button", report_dir)
            raise
        
        # Verify PayPal sandbox redirect and complete login
        try:
            print("\n--- Step 3: Completing PayPal Sandbox Login ---")
            # Wait for a new window/tab to open
            print("Waiting for PayPal sandbox window to open...")
            wait.until(lambda driver: len(driver.window_handles) > 1)
            # Switch to the new window/tab
            driver.switch_to.window(driver.window_handles[-1])
            
            # Verify we're on the PayPal sandbox page
            wait.until(
                lambda driver: "https://www.sandbox.paypal.com/checkoutnow?" in driver.current_url
            )
            print(f"Successfully redirected to PayPal sandbox: {driver.current_url}")
            take_screenshot(driver, "4-4", report_dir)
            
            # Enter email
            print("Entering PayPal email...")
            email_field = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='email']"))
            )
            email_field.clear()
            email_field.send_keys("xiaoxiqa@gmail.com")
            take_screenshot(driver, "4-5", report_dir)
            
            # Click Next button
            print("Clicking Next button...")
            next_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='btnNext']"))
            )
            next_button.click()
            take_screenshot(driver, "4-6", report_dir)
            
            # Wait for password field to be present and interactable
            print("Waiting for password field...")
            time.sleep(3)  # Additional wait for page transition
            
            # Try to find password field in main content and iframes
            password_field = None
            try:
                # First try in main content
                password_field = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='password']"))
                )
            except:
                # If not found, try in iframes
                print("Password field not found in main content, checking iframes...")
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                for iframe in iframes:
                    try:
                        driver.switch_to.frame(iframe)
                        password_field = wait.until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='password']"))
                        )
                        break
                    except:
                        driver.switch_to.default_content()
                        continue
            
            if password_field:
                print("Found password field, entering password...")
                # Wait for field to be interactable
                wait.until(EC.element_to_be_clickable(password_field))
                password_field.clear()
                password_field.send_keys("Xiaoxi123@")
                take_screenshot(driver, "4-7", report_dir)
                
                # Click Login button
                print("Clicking Login button...")
                login_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='btnLogin']"))
                )
                login_button.click()
                take_screenshot(driver, "4-8", report_dir)
                
                # Switch back to default content if we were in an iframe
                driver.switch_to.default_content()
                
                # Wait for payment review page and click Continue
                print("Waiting for payment review page...")
                wait.until(
                    lambda driver: "https://www.sandbox.paypal.com/webapps/hermes?" in driver.current_url
                )
                time.sleep(3)  # Additional wait for page to fully load
                
                print("Clicking Continue button...")
                # Try multiple selectors for the Continue button
                continue_button = None
                try:
                    # First try the new XPath
                    continue_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='hermione-container']/div[1]/main/div[3]/div[2]/button"))
                    )
                except:
                    try:
                        # Fallback to the old XPath
                        continue_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='button']/button"))
                        )
                    except:
                        # Try finding by text content
                        continue_button = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
                        )
                
                if continue_button:
                    # Scroll the button into view
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", continue_button)
                    time.sleep(1)
                    # Try JavaScript click first
                    try:
                        driver.execute_script("arguments[0].click();", continue_button)
                    except:
                        # Fallback to regular click
                        continue_button.click()
                    
                    take_screenshot(driver, "4-9", report_dir)
                else:
                    raise Exception("Could not find Continue button with any selector")
                
                # Wait for success page
                print("Waiting for payment success page...")
                wait.until(
                    lambda driver: "https://test-goproxy.xiaoxitech.com/dashboard/payment-success?payType=PayPal" in driver.current_url
                )
                
                # Verify success element is present
                print("Verifying success element...")
                success_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='__layout']/section/section/main/div/div/div[1]"))
                )
                print("Success element found!")
                take_screenshot(driver, "4-10", report_dir)
                
                return True
            else:
                raise Exception("Could not find password field in main content or iframes")
            
        except Exception as e:
            print(f"Failed to complete PayPal payment flow: {str(e)}")
            take_screenshot(driver, "error_paypal_payment_flow", report_dir)
            return False
            
    except Exception as e:
        print(f"\n=== Test failed with error: {str(e)} ===")
        take_screenshot(driver, "final_error", report_dir)
        raise

# ===== Main Test Function =====
def main():
    """Main function to run the complete test flow"""
    try:
        # Create a single report directory for the entire test run
        report_dir = create_report_dir()
        print(f"\n=== Starting test run with report directory: {report_dir} ===")
        
        # Run all test cases
        test_wallet_payment_with_balance(driver, report_dir)
        test_wallet_payment_without_balance(driver, report_dir)
        test_google_pay_payment(driver, report_dir)
        test_paypal_payment(driver, report_dir)
        
        # After all tests are complete, login to admin and close the package
        print("\n=== Starting admin operations after tests ===")
        login(report_dir)
        close_package(report_dir)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    report_dir = create_report_dir()
    print(f"\n=== Running all payment tests with report directory: {report_dir} ===")
    
    # Track test results
    test_results = {
        "wallet_payment_with_balance": "NOT_RUN",
        "wallet_payment_without_balance": "NOT_RUN", 
        "google_pay_payment": "NOT_RUN",
        "paypal_payment": "NOT_RUN",
        "admin_login": "NOT_RUN",
        "package_closure": "NOT_RUN"
    }
    
    try:
        # Test 1: Wallet payment with balance
        print("\n" + "="*60)
        print("TEST 1: WALLET PAYMENT WITH BALANCE")
        print("="*60)
        try:
            result = test_wallet_payment_with_balance(driver, report_dir)
            test_results["wallet_payment_with_balance"] = "PASSED" if result else "FAILED"
            print(f"✓ Test 1 completed: {test_results['wallet_payment_with_balance']}")
        except Exception as e:
            test_results["wallet_payment_with_balance"] = "FAILED"
            print(f"✗ Test 1 failed with error: {str(e)}")
            take_screenshot(driver, "test1_final_error", report_dir)
        
        # Test 2: Wallet payment without balance
        print("\n" + "="*60)
        print("TEST 2: WALLET PAYMENT WITHOUT BALANCE")
        print("="*60)
        try:
            result = test_wallet_payment_without_balance(driver, report_dir)
            test_results["wallet_payment_without_balance"] = "PASSED" if result else "FAILED"
            print(f"✓ Test 2 completed: {test_results['wallet_payment_without_balance']}")
        except Exception as e:
            test_results["wallet_payment_without_balance"] = "FAILED"
            print(f"✗ Test 2 failed with error: {str(e)}")
            take_screenshot(driver, "test2_final_error", report_dir)
        
        # Test 3: Google Pay payment
        print("\n" + "="*60)
        print("TEST 3: GOOGLE PAY PAYMENT")
        print("="*60)
        try:
            result = test_google_pay_payment(driver, report_dir)
            test_results["google_pay_payment"] = "PASSED" if result else "FAILED"
            print(f"✓ Test 3 completed: {test_results['google_pay_payment']}")
        except Exception as e:
            test_results["google_pay_payment"] = "FAILED"
            print(f"✗ Test 3 failed with error: {str(e)}")
            take_screenshot(driver, "test3_final_error", report_dir)
        
        # Test 4: PayPal payment
        print("\n" + "="*60)
        print("TEST 4: PAYPAL PAYMENT")
        print("="*60)
        try:
            result = test_paypal_payment(driver, report_dir)
            test_results["paypal_payment"] = "PASSED" if result else "FAILED"
            print(f"✓ Test 4 completed: {test_results['paypal_payment']}")
        except Exception as e:
            test_results["paypal_payment"] = "FAILED"
            print(f"✗ Test 4 failed with error: {str(e)}")
            take_screenshot(driver, "test4_final_error", report_dir)
        
        # Test 5: Admin login
        print("\n" + "="*60)
        print("TEST 5: ADMIN LOGIN")
        print("="*60)
        try:
            login(report_dir)
            test_results["admin_login"] = "PASSED"
            print("✓ Test 5 completed: PASSED")
        except Exception as e:
            test_results["admin_login"] = "FAILED"
            print(f"✗ Test 5 failed with error: {str(e)}")
            take_screenshot(driver, "test5_final_error", report_dir)
        
        # Test 6: Package closure (only if login succeeded)
        if test_results["admin_login"] == "PASSED":
            print("\n" + "="*60)
            print("TEST 6: PACKAGE CLOSURE")
            print("="*60)
            try:
                close_package(report_dir)
                test_results["package_closure"] = "PASSED"
                print("✓ Test 6 completed: PASSED")
            except Exception as e:
                test_results["package_closure"] = "FAILED"
                print(f"✗ Test 6 failed with error: {str(e)}")
                take_screenshot(driver, "test6_final_error", report_dir)
        else:
            test_results["package_closure"] = "SKIPPED"
            print("\n" + "="*60)
            print("TEST 6: PACKAGE CLOSURE - SKIPPED (Admin login failed)")
            print("="*60)
        
        # Print final test summary
        print("\n" + "="*60)
        print("FINAL TEST SUMMARY")
        print("="*60)
        passed_count = sum(1 for result in test_results.values() if result == "PASSED")
        failed_count = sum(1 for result in test_results.values() if result == "FAILED")
        skipped_count = sum(1 for result in test_results.values() if result == "SKIPPED")
        
        for test_name, result in test_results.items():
            status_icon = "✓" if result == "PASSED" else "✗" if result == "FAILED" else "⚠"
            print(f"{status_icon} {test_name.replace('_', ' ').title()}: {result}")
        
        print(f"\nOverall Results:")
        print(f"  Passed: {passed_count}")
        print(f"  Failed: {failed_count}")
        print(f"  Skipped: {skipped_count}")
        print(f"  Total: {len(test_results)}")
        print(f"\nTest reports saved in: {report_dir}")
        
    finally:
        print("\n=== Cleaning up and closing browser ===")
        driver.quit() 