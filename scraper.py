import datetime

from RPA.Excel.Files import Files
from dateutil.relativedelta import relativedelta
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from browser import Browser
from exceptions import DateLimitReachException
from models import News
from utils import convert_string_to_date_time, OUTPUT_PATH, logger


class NewsScraper:

    def __init__(self, search_phrase: str, topics: list = None, month: int = 0):
        self.browser = Browser()
        self.url = 'https://www.latimes.com/'
        self.news_list = []
        self.search_text: str = search_phrase
        self.month = 1 if not month else month
        self.date_range = datetime.datetime.today() - relativedelta(months=self.month)
        self.topics = topics if topics else []

    def open_news_site(self):
        if self.browser.driver.location == self.url:
            return None
        else:
            self.browser.open_site(url=self.url, page_load_time=20)

    def search_news(self):
        self.browser.click_element('//button[@data-element="search-button"]')
        self.browser.input_text('//input[@data-element="search-form-input"]', self.search_text)
        self.browser.driver.press_keys('//input[@data-element="search-form-input"]', Keys.ENTER)

    def sort_news(self, order: str = "1"):
        self.browser.select_dropdown_option_by_value('//select[@class="select-input"]', order)

    def select_topic(self):
        for topic in self.topics:
            topic_locator = f"//span[text()='{topic}']//preceding-sibling::input"
            if self.browser.check_if_element_exists(topic_locator):
                logger.info(f'applying {topic}')
                self.browser.click_element('//p[text()="Topics"]//ancestor::ps-toggler//button[@class="button see-all-button"]')
                self.browser.click_element('//p[text()="Type"]//ancestor::ps-toggler//button[@class="button see-all-button"]')
                self.browser.select_check_box(topic_locator)
                try:
                    self.browser.driver.wait_until_element_is_visible("//div[@class='loading-icon']")
                    self.browser.driver.wait_until_element_is_not_visible("//div[@class='loading-icon']")
                except AssertionError:
                    ...

    def handle_promo_pop_up(self):
        self.browser.driver.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if self.browser.check_if_element_exists('//modality-custom-element'):
            element = self.browser.get_element('//modality-custom-element')
            close_button = self.browser.driver.driver.execute_script('return arguments[0].shadowRoot.querySelector("a")', element)
            close_button.click()

    def check_if_last_page(self):
        page_counts = self.browser.get_element('//div[@class="search-results-module-page-counts"]').text
        current_page, last_page = [text.strip() for text in page_counts.split("of")]
        return current_page == last_page

    def go_to_next_page(self):
        next_page_button = self.browser.get_element('//div[@class="search-results-module-next-page"]')
        next_page_button.click()

    def scrap_news(self):
        start = 0
        while True:
            news_elements = self.browser.get_elements('//ul[@class="search-results-module-results-menu"]//li')
            start = start + len(news_elements)
            logger.info(f'scraping {start} news')
            for index, news in enumerate(news_elements, 1):
                logger.info(f'scrapped news at {start + index - 10}')
                title = news.find_element(By.XPATH, './/a[@class="link"]')
                desc = news.find_element(By.XPATH, './/p[@class="promo-description"]')
                img = news.find_element(By.XPATH, './/img[@class="image"]')
                time_stamp = news.find_element(By.XPATH, './/p[@class="promo-timestamp"]')
                if convert_string_to_date_time(time_stamp.text) < self.date_range:
                    raise DateLimitReachException
                self.news_list.append(
                    News(
                        title=title.text,
                        time_stamp=time_stamp.text,
                        img_url=img.get_attribute('src'),
                        description=desc.text)
                )

            if self.check_if_last_page():
                break
            else:
                self.go_to_next_page()

    def dump_report(self):
        rows = []
        for news in self.news_list:
            rows.append({
                "Title": news.title,
                "Desc": news.description,
                "Date": news.time_stamp,
                "file_name": news.file_name,
                "Search Phrase Count": news.search_phrase_count(self.search_text),
                "Does Contains Amount": str(news.check_if_contains_amount()),
            })
        writer = Files()
        writer.create_workbook(OUTPUT_PATH + "report.xlsx")
        writer.create_worksheet('News')
        writer.append_rows_to_worksheet(rows, header=True)
        writer.save_workbook()

    def process(self):
        logger.info('Starting process')
        try:
            logger.info('Opening news site')
            self.open_news_site()
            logger.info('Searching phrase')
            self.search_news()
            logger.info('Sorting newest news')
            self.sort_news()
            logger.info('Handling promo pop up')
            self.handle_promo_pop_up()
            logger.info('Applying topic filter')
            self.select_topic()
            logger.info('Scraping news')
            self.scrap_news()
        except DateLimitReachException:
            ...
        finally:
            logger.info('Creating report')
            self.dump_report()
        logger.info('Process finished')
