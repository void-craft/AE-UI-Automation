import os
import allure
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """Base page class with common functionality for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)
    
    # Navigation methods
    def navigate_to(self, url):
        """Navigate to a specific URL"""
        with allure.step(f"Navigate to URL: {url}"):
            self.driver.get(url)
            self.wait_for_page_load()
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    def refresh_page(self):
        """Refresh the current page"""
        with allure.step("Refresh page"):
            self.driver.refresh()
            self.wait_for_page_load()
    
    def go_back(self):
        """Navigate back in browser history"""
        with allure.step("Navigate back"):
            self.driver.back()
            self.wait_for_page_load()
    
    # Element interaction methods
    def find_element(self, locator, timeout=10):
        """Find a single element with explicit wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.take_screenshot(f"element_not_found_{locator[1]}")
            raise TimeoutException(f"Element not found: {locator}")
    
    def find_elements(self, locator, timeout=10):
        """Find multiple elements with explicit wait"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            self.take_screenshot(f"elements_not_found_{locator[1]}")
            raise TimeoutException(f"Elements not found: {locator}")
    
    def click_element(self, locator, timeout=10):
        """Click an element with explicit wait"""
        with allure.step(f"Click element: {locator[1]}"):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
            except TimeoutException:
                self.take_screenshot(f"click_failed_{locator[1]}")
                raise TimeoutException(f"Element not clickable: {locator}")
    
    def enter_text(self, locator, text, clear_first=True, timeout=10):
        """Enter text into an input field"""
        with allure.step(f"Enter text '{text}' into element: {locator[1]}"):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                if clear_first:
                    element.clear()
                element.send_keys(text)
            except TimeoutException:
                self.take_screenshot(f"text_entry_failed_{locator[1]}")
                raise TimeoutException(f"Cannot enter text in element: {locator}")
    
    def get_element_text(self, locator, timeout=10):
        """Get text from an element"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.text
        except TimeoutException:
            self.take_screenshot(f"get_text_failed_{locator[1]}")
            raise TimeoutException(f"Cannot get text from element: {locator}")
    
    def get_element_attribute(self, locator, attribute, timeout=10):
        """Get attribute value from an element"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.get_attribute(attribute)
        except TimeoutException:
            self.take_screenshot(f"get_attribute_failed_{locator[1]}")
            raise TimeoutException(f"Cannot get attribute from element: {locator}")
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present on the page"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible on the page"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_clickable(self, locator, timeout=5):
        """Check if element is clickable"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return True
        except TimeoutException:
            return False
    
    # Wait methods
    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for element to be visible"""
        with allure.step(f"Wait for element to be visible: {locator[1]}"):
            try:
                return WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
            except TimeoutException:
                self.take_screenshot(f"wait_visible_failed_{locator[1]}")
                raise TimeoutException(f"Element not visible: {locator}")
    
    def wait_for_element_invisible(self, locator, timeout=10):
        """Wait for element to be invisible"""
        with allure.step(f"Wait for element to be invisible: {locator[1]}"):
            try:
                return WebDriverWait(self.driver, timeout).until(
                    EC.invisibility_of_element_located(locator)
                )
            except TimeoutException:
                self.take_screenshot(f"wait_invisible_failed_{locator[1]}")
                raise TimeoutException(f"Element still visible: {locator}")
    
    def wait_for_text_in_element(self, locator, text, timeout=10):
        """Wait for specific text to appear in element"""
        with allure.step(f"Wait for text '{text}' in element: {locator[1]}"):
            try:
                return WebDriverWait(self.driver, timeout).until(
                    EC.text_to_be_present_in_element(locator, text)
                )
            except TimeoutException:
                self.take_screenshot(f"wait_text_failed_{locator[1]}")
                raise TimeoutException(f"Text '{text}' not found in element: {locator}")
    
    def wait_for_page_load(self, timeout=30):
        """Wait for page to fully load"""
        with allure.step("Wait for page to load"):
            try:
                WebDriverWait(self.driver, timeout).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
            except TimeoutException:
                self.take_screenshot("page_load_timeout")
                raise TimeoutException("Page load timeout")
    
    def wait_for_url_contains(self, text, timeout=10):
        """Wait for URL to contain specific text"""
        with allure.step(f"Wait for URL to contain: {text}"):
            try:
                return WebDriverWait(self.driver, timeout).until(
                    EC.url_contains(text)
                )
            except TimeoutException:
                self.take_screenshot(f"url_wait_failed_{text}")
                raise TimeoutException(f"URL does not contain: {text}")
    
    # Screenshot methods
    def take_screenshot(self, name=None):
        """Take a screenshot and attach to Allure report"""
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}"
        
        # Create screenshots directory if it doesn't exist
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Take screenshot
        screenshot_path = os.path.join(screenshots_dir, f"{name}.png")
        self.driver.save_screenshot(screenshot_path)
        
        # Attach to Allure report
        try:
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=f"Screenshot: {name}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Failed to attach screenshot to Allure: {e}")
        
        return screenshot_path
    
    def take_element_screenshot(self, locator, name=None):
        """Take screenshot of a specific element"""
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"element_screenshot_{timestamp}"
        
        try:
            element = self.find_element(locator)
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            
            screenshot_path = os.path.join(screenshots_dir, f"{name}.png")
            element.screenshot(screenshot_path)
            
            # Attach to Allure report
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=f"Element Screenshot: {name}",
                    attachment_type=allure.attachment_type.PNG
                )
            
            return screenshot_path
        except Exception as e:
            print(f"Failed to take element screenshot: {e}")
            return self.take_screenshot(name)
    
    # Browser actions
    def scroll_to_element(self, locator):
        """Scroll to a specific element"""
        with allure.step(f"Scroll to element: {locator[1]}"):
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        with allure.step("Scroll to top of page"):
            self.driver.execute_script("window.scrollTo(0, 0);")
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        with allure.step("Scroll to bottom of page"):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def hover_over_element(self, locator):
        """Hover over an element"""
        with allure.step(f"Hover over element: {locator[1]}"):
            element = self.find_element(locator)
            self.actions.move_to_element(element).perform()
    
    def double_click_element(self, locator):
        """Double click an element"""
        with allure.step(f"Double click element: {locator[1]}"):
            element = self.find_element(locator)
            self.actions.double_click(element).perform()
    
    def right_click_element(self, locator):
        """Right click an element"""
        with allure.step(f"Right click element: {locator[1]}"):
            element = self.find_element(locator)
            self.actions.context_click(element).perform()
    
    # JavaScript execution
    def execute_javascript(self, script, *args):
        """Execute JavaScript code"""
        with allure.step(f"Execute JavaScript: {script[:50]}..."):
            return self.driver.execute_script(script, *args)
    
    # Alert handling
    def handle_alert(self, action="accept"):
        """Handle JavaScript alerts"""
        with allure.step(f"Handle alert - action: {action}"):
            try:
                alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                alert_text = alert.text
                allure.attach(alert_text, name="Alert Text", attachment_type=allure.attachment_type.TEXT)
                
                if action.lower() == "accept":
                    alert.accept()
                elif action.lower() == "dismiss":
                    alert.dismiss()
                
                return alert_text
            except TimeoutException:
                raise TimeoutException("No alert present")
    
    # Window handling
    def switch_to_window(self, window_handle):
        """Switch to a specific browser window"""
        with allure.step(f"Switch to window: {window_handle}"):
            self.driver.switch_to.window(window_handle)
    
    def get_window_handles(self):
        """Get all window handles"""
        return self.driver.window_handles
    
    def close_current_window(self):
        """Close current browser window"""
        with allure.step("Close current window"):
            self.driver.close()
    
    # Frame handling
    def switch_to_frame(self, frame_locator):
        """Switch to iframe"""
        with allure.step(f"Switch to frame: {frame_locator}"):
            frame = self.find_element(frame_locator)
            self.driver.switch_to.frame(frame)
    
    def switch_to_default_content(self):
        """Switch back to main content from iframe"""
        with allure.step("Switch to default content"):
            self.driver.switch_to.default_content()
    
    # Utility methods
    def get_page_source(self):
        """Get page source HTML"""
        return self.driver.page_source
    
    def clear_browser_cache(self):
        """Clear browser cache"""
        with allure.step("Clear browser cache"):
            self.driver.delete_all_cookies()
    
    def set_window_size(self, width, height):
        """Set browser window size"""
        with allure.step(f"Set window size: {width}x{height}"):
            self.driver.set_window_size(width, height)
    
    def maximize_window(self):
        """Maximize browser window"""
        with allure.step("Maximize window"):
            self.driver.maximize_window()
    
    def minimize_window(self):
        """Minimize browser window"""
        with allure.step("Minimize window"):
            self.driver.minimize_window()
    
    # Validation methods
    def assert_element_text(self, locator, expected_text, timeout=10):
        """Assert element contains expected text"""
        with allure.step(f"Assert element text equals '{expected_text}'"):
            actual_text = self.get_element_text(locator, timeout)
            assert actual_text == expected_text, f"Expected '{expected_text}', but got '{actual_text}'"
    
    def assert_element_contains_text(self, locator, expected_text, timeout=10):
        """Assert element contains expected text"""
        with allure.step(f"Assert element contains text '{expected_text}'"):
            actual_text = self.get_element_text(locator, timeout)
            assert expected_text in actual_text, f"Text '{expected_text}' not found in '{actual_text}'"
    
    def assert_page_title(self, expected_title):
        """Assert page title"""
        with allure.step(f"Assert page title equals '{expected_title}'"):
            actual_title = self.get_page_title()
            assert actual_title == expected_title, f"Expected title '{expected_title}', but got '{actual_title}'"
    
    def assert_current_url(self, expected_url):
        """Assert current URL"""
        with allure.step(f"Assert current URL equals '{expected_url}'"):
            actual_url = self.get_current_url()
            assert actual_url == expected_url, f"Expected URL '{expected_url}', but got '{actual_url}'"
    
    def assert_url_contains(self, expected_text):
        """Assert URL contains expected text"""
        with allure.step(f"Assert URL contains '{expected_text}'"):
            actual_url = self.get_current_url()
            assert expected_text in actual_url, f"Text '{expected_text}' not found in URL '{actual_url}'"