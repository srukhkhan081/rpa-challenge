from RPA.Browser.Selenium import Selenium
from selenium.webdriver.chrome.options import Options

from decorators import page_load, wait_element


class Browser:
    """
    Class representing a browser.
    """

    def __init__(self):
        """
        Initialize the Browser object.
        """
        self.driver = Selenium()
        self.setup_browser()
        self.timeouts = self.driver.driver.timeouts

    def setup_browser(self):
        """
        Set up the browser with specified options.
        """
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        self.driver.open_available_browser(maximized=True, options=chrome_options, headless=True)

    @page_load
    def open_site(self, url: str, **kwargs):
        """
        Open a website in the browser.

        Args:
            url (str): The URL of the website to open.
            **kwargs: Additional keyword arguments.
        """
        self.driver.go_to(url)

    @wait_element
    def click_element(self, locator, **kwargs):
        """
        Click on an element identified by the locator.

        Args:
            locator: The locator of the element to click.
            **kwargs: Additional keyword arguments.
        """
        element = self.driver.find_element(locator)
        element.click()

    @wait_element
    def input_text(self, locator: str, text: str):
        """
        Input text into an element identified by the locator.

        Args:
            locator (str): The locator of the element.
            text (str): The text to input.
        """
        self.driver.clear_element_text(locator)
        self.driver.input_text(locator, text)

    @wait_element
    def select_dropdown_option_by_value(self, locator: str, value: str):
        """
        Select a dropdown option by its value.

        Args:
            locator (str): The locator of the dropdown element.
            value (str): The value of the option to select.
        """
        self.driver.select_from_list_by_value(locator, value)

    @wait_element
    def select_check_box(self, locator: str):
        """
        Select a checkbox identified by the locator.

        Args:
            locator (str): The locator of the checkbox.
        """
        self.driver.select_checkbox(locator)

    def check_if_element_exists(self, locator: str):
        """
        Check if an element identified by the locator exists on the page.

        Args:
            locator (str): The locator of the element.

        Returns:
            bool: True if the element exists, False otherwise.
        """
        try:
            self.driver.wait_until_page_contains_element(locator)
            return True
        except:
            return False

    @wait_element
    def get_element(self, locator: str):
        """
        Get a single element identified by the locator.

        Args:
            locator (str): The locator of the element.

        Returns:
            WebElement: The web element.
        """
        return self.driver.find_element(locator)

    @wait_element
    def get_elements(self, locator: str):
        """
        Get multiple elements identified by the locator.

        Args:
            locator (str): The locator of the elements.

        Returns:
            List[WebElement]: List of web elements.
        """
        return self.driver.find_elements(locator)
