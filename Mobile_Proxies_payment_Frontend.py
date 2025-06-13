"""
Selenium Test Automation for Payment System - Mobile Proxies
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
    test_dir = os.path.join(report_dir, f"Mobile_Proxies_test_run_{timestamp}")
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
                "Admin_Token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHQiOiJ7XCJhY3RpdmVcIjp0cnVlLFwibG9naW5fZmxhZ1wiOlwiMjFmYmI2YTFjMGNjMjVjNWEzNjkzMDgyMTNiM2QwOTZcIn0iLCJ1c2VyX25hbWUiOiJhbWFuZGExQGdldG5hZGEuY29tIiwic2NvcGUiOlsiYWxsIl0sImV4cCI6MTc1MDMxNzY5OSwidXNlcklkIjoiMTkyNDM3NTE4Nzc1OTk1NTk2OCIsImp0aSI6IjlkYWE3MzMwLWM1NzMtNGQ4OC05YzQ0LTlmNWIyMTZmN2M1OSIsImNsaWVudF9pZCI6ImdvX3Byb3h5In0.CirGEnccmr7RgrkZKXXJJvjdEgVjk-CoxnANdGMfiNVOSs3DhiEUSv0cJ2mn7WNaheNA1vzno5NLsAuQ39hmTJGANGqB-__0YXxE50PhhwUDzYPit-xLBCDCqWyHDitcc1bbBy6IMQlEQAVx3PLYLioyiOTbMiuUaNgyf3tBW1O48HlD0gbKfVelxvq6zY9qd4dIn3Ih0m4tyN_OmlE-HWP8eYLvWShIkjxq5c8YXgcDvP5CEt90N2ihyy0G6KHg4KCn-4nnaPxonHNKNiSH51JZkSVTmfsjor4g7h4wzmpzKaqB-BNyq8cLB1DKOqEj68TnR2iy6vDdewXMyfzE7g"
            }
        else:  # without_balance
            cookies = {
                "Admin_Token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHQiOiJ7XCJhY3RpdmVcIjp0cnVlLFwibG9naW5fZmxhZ1wiOlwiY2RlNDQ2OTIyZDBmMjRkZTMyMGEyNGYyZWU2OTA0MDhcIn0iLCJ1c2VyX25hbWUiOiJhbWFuZGEyQGdldG5hZGEuY29tIiwic2NvcGUiOlsiYWxsIl0sImV4cCI6MTc1MDM4NDMwMywidXNlcklkIjoiMTkyNDY1ODAxNjExNjkzMjYwOCIsImp0aSI6ImZiMGUzOGYzLTBiZGMtNDA1YS04MWViLTI2OGE1YTQ0NDg1MCIsImNsaWVudF9pZCI6ImdvX3Byb3h5In0.iT1mjSdRorZFS6OaPIUdmVmOpP6nxh6bFe5xuNXwIiXEKjCJjay0BceiGqNjyr7pzTZYlVH1sRiFXjUnDQYU38NF4beC23fXeReH0id172psiUn2Dk5ixSXsOdlbdentxeGqC_c0cVlehMgXRknXAvDM1NHsfusnjqD4Sz0kf_coA_V1d4kATGaSIoXroAa2VKBiCfousr0XApBInOP85c_xMIo7knF55hIHnKV1uJieIqtIkk4Hvz_D9gR2qqb67NSrt9kGZTQGgLVjSGMh1cXTlgY18dY2va3Ah5PrY6XO7_9m3QwHO_-6GvQk3dZl-clCMCwzSUsOTN6X9XW9sg"
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

def test_wallet_payment_with_balance(driver, report_dir):
    """Test case for wallet payment with sufficient balance"""
    try:
        print("\n=== Starting wallet payment with balance test ===")
        # Add authentication cookies
        add_auth_cookies(driver, "with_balance", report_dir)
        
        # Navigate to the payment page
        driver.get("https://test-goproxy.xiaoxitech.com/dashboard/pay/dynamicResidence?mealId=1828699653267464194&mealType=5")
        
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
        
        # Navigate to the payment page
        driver.get("https://test-goproxy.xiaoxitech.com/dashboard/pay/dynamicResidence?mealId=1828699653267464194&mealType=5")
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
        
        # Navigate to the payment page
        driver.get("https://test-goproxy.xiaoxitech.com/dashboard/pay/dynamicResidence?mealId=1828699653267464194&mealType=5")
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
if __name__ == "__main__":
    report_dir = create_report_dir()
    print(f"\n=== Running all mobile proxies payment tests with report directory: {report_dir} ===")
    
    # Track test results
    test_results = {
        "wallet_payment_with_balance": "NOT_RUN",
        "wallet_payment_without_balance": "NOT_RUN", 
        "google_pay_payment": "NOT_RUN",
        "paypal_payment": "NOT_RUN"
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
        
        # Print final test summary
        print("\n" + "="*60)
        print("FINAL TEST SUMMARY - MOBILE PROXIES PAYMENTS")
        print("="*60)
        passed_count = sum(1 for result in test_results.values() if result == "PASSED")
        failed_count = sum(1 for result in test_results.values() if result == "FAILED")
        
        for test_name, result in test_results.items():
            status_icon = "✓" if result == "PASSED" else "✗" if result == "FAILED" else "⚠"
            print(f"{status_icon} {test_name.replace('_', ' ').title()}: {result}")
        
        print(f"\nOverall Results:")
        print(f"  Passed: {passed_count}")
        print(f"  Failed: {failed_count}")
        print(f"  Total: {len(test_results)}")
        print(f"\nTest reports saved in: {report_dir}")
        
    finally:
        print("\n=== Cleaning up and closing browser ===")
        driver.quit() 