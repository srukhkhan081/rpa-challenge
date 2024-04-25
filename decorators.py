from selenium.common import TimeoutException


def page_load(func):
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
    def wrapper(*args, **kwargs):
        self = args[0]
        locator = args[1]
        self.driver.wait_until_page_contains_element(locator)
        self.driver.scroll_element_into_view(locator)
        return func(*args, **kwargs)
    return wrapper


def handle_promo_pop_up(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.check_if_element_exists('//modality-custom-element'):
            element = self.driver.find_element('//modality-custom-element')
            close_button = self.driver.driver.execute_script('return arguments[0].shadowRoot.querySelector("a")',
                                                             element)
            close_button.click()
        return func(*args, **kwargs)
    return wrapper