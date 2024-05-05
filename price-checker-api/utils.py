from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    # Create an instance of Options
    options = Options()

    # Start the browser maximized to avoid missing elements due to smaller viewports
    options.add_argument("start-maximized")

    # Set the User-Agent string to mimic a real user
    # This can help avoid detection by websites that block scrapers
    options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')

    # Disable Selenium flags to make automation less detectable
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Prevent the website from detecting that the browser is being controlled by automation software
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Set up the ChromeDriver to manage the version of the driver automatically
    # This ensures the driver matches the version of Chrome installed on the system
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Return the configured WebDriver instance
    return driver
