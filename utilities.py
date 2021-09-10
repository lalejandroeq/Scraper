import logging
import re
import time
import csv
import random
# Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from .settings import CHROMEDRIVER_PATH
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)


class Crawler:
    def __init__(self, url, log):
        self.url = url
        self.log = log
        self._browser = None

    def _open_browser(self):
        # CHROMEDRIVER_PATH = '../chromedriver.exe'
        options = Options()
        options.headless = True
        options.add_argument("user-agent=Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
        options.add_argument("--log-level=1")
        options.add_argument('window-size=1920x1080')
        self._browser = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

    def close(self):
        if self._browser is not None:
            self._browser.close()

    def load_page(self, url=None, wait_element=None):
        if url is None:
            url = self.url
        if self._browser is None:
            self._open_browser()
        try:
            self._browser.get(url)
        except Exception as e:
            self.log("Error while loading page {} {}".format(url, e))
        if wait_element is not None:
            try:
                WebDriverWait(self._browser, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,
                                                                                                    wait_element)))
            except TimeoutException:
                self._browser.close()
                raise Exception("Timeout has been reached while loading page {}".format(url))
        self.log("Page {} has been loaded successfully".format(url))
        self.url = self._browser.current_url

    def submit_form(self, submit_class, form_dictionary=None):
        if self._browser is None:
            self._open_browser()
        # Handle form
        if form_dictionary is not None:
            print(form_dictionary)
            for element, value in form_dictionary.items():
                # Fill form
                try:
                    browser_element = self._browser.find_element_by_name(element)
                    browser_element.send_keys(value)
                except Exception:
                    self._browser.close()
                    raise Exception("Error while trying to find form element {}".format(element))
        # Find submit button by class and click it
        try:
            self._browser.find_element_by_class_name(submit_class).click()
        except Exception:
            self._browser.close()
            raise Exception("Error while trying to find submit button {}".format(submit_class))
        time.sleep(random.randint(1, 3))  # Implicit wait
        self.url = self._browser.current_url

    def paginate(self, stop_at=None):
        if self._browser is None:
            self._open_browser()
        self.log("Crawling page {}".format(1))
        yield self._browser
        counter = 2
        while True:
            # Handle stop page
            if stop_at is not None and counter > stop_at:
                self.log("Stopped at page {}".format(counter - 1))
                return self._browser
            self.log("Crawling page {}".format(counter))
            try:
                time.sleep(random.randint(1, 3))  # Implicit wait
                # Find page by value and click it
                next_page = self._browser.find_element_by_link_text(str(counter))
                print(next_page)
                next_page.click()
                self.url = self._browser.current_url
            except Exception as e:
                error_msg = "No more pages to crawl, stopped at {}".format(counter)
                if counter == 2:
                    error_msg = "Pagination has not been found in page {} error {}".format(self._browser.current_url,
                                                                                           e)
                print(error_msg)
                return self._browser
            yield self._browser
            counter += 1

    def get_links(self, link_class):
        if self._browser is None:
            self._open_browser()
        # Get all links in a page with defined element class
        self.log("Capturing every link with element class {}".format(link_class))
        try:
            links = [link.get_attribute("href") for link in self._browser.find_elements_by_class_name(link_class)
                     if link.get_attribute("href") is not None]
        except Exception:
            self._browser.close()
            raise Exception("Error while trying to get links {}".format(link_class))
        self.log("Successfully captured all links")
        return links


def get_table_data(soup, table_class):
    table_data = {}
    try:
        table = soup.find("table", attrs={"class": table_class})
    except Exception as e:
        raise Exception("Error while searching for table class {} with error {}".format(table_class, e))
    table_body = table.find("tbody")
    rows = table_body.find_all("tr")
    other_counter = 1
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        row = [ele for ele in cols if ele]
        if len(row) == 1:
            row.insert(0, "Otro{}".format(other_counter))
            other_counter += 1
        table_data[row[0]] = row[1]  # Get rid of empty values
    return table_data


def read_csv(file_name):
    with open(file_name, "r", newline="") as f:
        csv_data = list(csv.reader(f))
        return csv_data


def get_currency(text):
    try:
        currency = re.search(r'([¢₡£$€])', text).group(1)
    except AttributeError:
        currency = '$'
    if currency in ['¢', '₡']:
        currency = '₡'
    return currency


def string_to_int(text):
    text = text.strip()
    try:
        output = re.sub("[^0-9]", "", text)
    except ValueError:
        output = 'N/A'
    if len(output.strip()) == 0:
        output = 'N/A'
    return output


if __name__ == '__main__':
    # crawler = Crawler('https://crautos.com/autosusados/', print)
    # crawler.load_page()
    # crawler.submit_form('btn.btn-sm.btn-success', {'yearfrom': '2010'})
    # urls = []
    # for _ in crawler.paginate(stop_at=5):
    #     page_urls = crawler.get_links('inventory')
    #     urls.extend(page_urls)
    # crawler.close()

    test_text = '₡  1,000'
    print(get_currency(test_text))
