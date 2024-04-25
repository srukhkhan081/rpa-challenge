from RPA.Browser.Selenium import Selenium
from selenium.webdriver.chrome.options import Options

from decorators import page_load, wait_element


class Browser:

    def __init__(self):
        self.driver = Selenium()
        self.setup_browser()
        self.timeouts = self.driver.driver.timeouts

    def setup_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        self.driver.open_available_browser(maximized=True, options=chrome_options, headless=True)

    @page_load
    def open_site(self, url: str, **kwargs):
        self.driver.go_to(url)

    @wait_element
    def click_element(self, locator, **kwargs):
        element = self.driver.find_element(locator)
        element.click()

    @wait_element
    def input_text(self, locator: str, text: str):
        self.driver.clear_element_text(locator)
        self.driver.input_text(locator, text)

    @wait_element
    def select_dropdown_option_by_value(self, locator: str, value: str):
        self.driver.select_from_list_by_value(locator, value)

    @wait_element
    def select_check_box(self, locator: str):
        self.driver.select_checkbox(locator)

    def check_if_element_exists(self, locator: str):
        try:
            self.driver.wait_until_page_contains_element(locator)
            return True
        except:
            return False

    @wait_element
    def get_element(self, locator: str):
        return self.driver.find_element(locator)

    @wait_element
    def get_elements(self, locator: str):
        return self.driver.find_elements(locator)

