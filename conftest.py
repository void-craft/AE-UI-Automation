import os
import pytest
import allure
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from utils.config import Config


def pytest_addoption(parser):
    """Add command line options for pytest"""
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome", 
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless", 
        action="store_true", 
        default=False, 
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--window-size", 
        action="store", 
        default="1920,1080", 
        help="Browser window size (width,height)"
    )


@pytest.fixture(scope="session")
def config():
    """Load configuration"""
    return Config()


@pytest.fixture(scope="function")
def driver(request, config):
    """Create and manage WebDriver instance"""
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    window_size = request.config.getoption("--window-size")
    
    # Parse window size
    width, height = map(int, window_size.split(','))
    
    # Set up browser options
    driver_instance = None
    
    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")  # Remove if JS is needed
        chrome_options.add_argument(f"--window-size={width},{height}")
        
        if headless or os.getenv("CI"):  # Always headless in CI
            chrome_options.add_argument("--headless")
        
        # Set up logging
        chrome_options.add_argument("--log-level=3")  # Suppress console logs
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        driver_instance = webdriver.Chrome(options=chrome_options)
        
    elif browser == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument(f"--width={width}")
        firefox_options.add_argument(f"--height={height}")
        
        if headless or os.getenv("CI"):
            firefox_options.add_argument("--headless")
        
        driver_instance = webdriver.Firefox(options=firefox_options)
    
    else:
        raise ValueError(f"Browser '{browser}' is not supported")
    
    # Configure driver
    driver_instance.implicitly_wait(10)
    driver_instance.maximize_window()
    
    # Add driver info to Allure report
    allure.attach(
        name="Browser Info",
        body=f"Browser: {browser.title()}\nHeadless: {headless}\nWindow Size: {window_size}",
        attachment_type=allure.attachment_type.TEXT
    )
    
    yield driver_instance
    
    # Cleanup
    if driver_instance:
        driver_instance.quit()


@pytest.fixture(scope="function")
def take_screenshot(driver, request):
    """Fixture to take screenshot on test failure"""
    def _take_screenshot(name=None):
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = request.node.name
            name = f"{test_name}_{timestamp}"
        
        # Create screenshots directory if it doesn't exist
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Take screenshot
        screenshot_path = os.path.join(screenshots_dir, f"{name}.png")
        driver.save_screenshot(screenshot_path)
        
        # Attach to Allure report
        with open(screenshot_path, "rb") as image_file:
            allure.attach(
                image_file.read(),
                name=f"Screenshot: {name}",
                attachment_type=allure.attachment_type.PNG
            )
        
        return screenshot_path
    
    return _take_screenshot


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Get the driver from the test's fixtures
        if hasattr(item, '_request') or hasattr(item.instance, 'driver' if hasattr(item, 'instance') else None):
            try:
                # Try to get driver from fixture
                driver = item.funcargs.get('driver') if hasattr(item, 'funcargs') else None
                
                if driver:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    test_name = item.name.replace("[", "_").replace("]", "_")
                    screenshot_name = f"FAILED_{test_name}_{timestamp}"
                    
                    # Create screenshots directory
                    screenshots_dir = "screenshots"
                    os.makedirs(screenshots_dir, exist_ok=True)
                    
                    # Take screenshot
                    screenshot_path = os.path.join(screenshots_dir, f"{screenshot_name}.png")
                    driver.save_screenshot(screenshot_path)
                    
                    # Attach to Allure
                    try:
                        with open(screenshot_path, "rb") as image_file:
                            allure.attach(
                                image_file.read(),
                                name=f"Failure Screenshot: {test_name}",
                                attachment_type=allure.attachment_type.PNG
                            )
                    except Exception as e:
                        print(f"Failed to attach screenshot to Allure: {e}")
                    
                    # Add screenshot path to test report
                    setattr(item, 'screenshot_path', screenshot_path)
                    
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")


def pytest_configure(config):
    """Configure pytest with custom markers and setup"""
    # Register custom markers
    config.addinivalue_line(
        "markers", "smoke: marks tests as smoke tests"
    )
    config.addinivalue_line(
        "markers", "regression: marks tests as regression tests"
    )
    config.addinivalue_line(
        "markers", "login: marks tests related to login functionality"
    )
    config.addinivalue_line(
        "markers", "registration: marks tests related to registration functionality"
    )
    
    # Set up Allure environment info
    allure_results_dir = config.getoption("--alluredir")
    if allure_results_dir:
        os.makedirs(allure_results_dir, exist_ok=True)
        
        # Create environment.properties file for Allure
        env_props_path = os.path.join(allure_results_dir, "environment.properties")
        with open(env_props_path, "w") as f:
            f.write(f"Base.URL={os.getenv('BASE_URL', 'https://automationexercise.com')}\n")
            f.write(f"Browser={config.getoption('--browser', 'chrome')}\n")
            f.write(f"Headless={config.getoption('--headless', False)}\n")
            f.write(f"Python.Version={os.sys.version}\n")
            f.write(f"Platform={os.name}\n")


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment"""
    # Create necessary directories
    directories = ["screenshots", "test-reports", "allure-results"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Set environment variables for tests
    os.environ.setdefault("PYTHONPATH", os.getcwd())
    
    yield
    
    # Cleanup after all tests
    print("\n🧹 Test execution completed. Cleaning up...")


@pytest.fixture
def base_url(config):
    """Get base URL from config"""
    return config.BASE_URL


# Utility fixtures for common test data
@pytest.fixture
def valid_user_credentials(config):
    """Get valid user credentials"""
    return {
        "email": config.AE_USERNAME,
        "password": config.AE_PASSWORD
    }


@pytest.fixture
def invalid_user_credentials():
    """Get invalid user credentials for negative testing"""
    return {
        "email": "invalid@example.com",
        "password": "wrongpassword"
    }