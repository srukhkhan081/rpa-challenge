from selenium.common import TimeoutException


def page_load(func):
    """
    Decorator to handle page load timeouts.
    """
    def wrapper(*args, **kwargs):
        self = args[0]
        page_load_time = kwargs.get('page_load_time')
        self.driver.driver.set_page_load_timeout(page_load_time if page_load_time else self.timeouts.page_load)
        try:
            return func(*args, **kwargs)
        except TimeoutException:
            self.driver.execute_javascript("window.stop();")
        self.driver.driver.set_page_load_timeout(self.timeouts.page_load)
    return wrapper


def wait_element(func):
    """
    Decorator to wait for an element to be present on the page.
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function to wait for an element to be present on the page.
        """
        self = args[0]
        locator = args[1]
        self.driver.wait_until_page_contains_element(locator)
        self.driver.scroll_element_into_view(locator)
        return func(*args, **kwargs)
    return wrapper
