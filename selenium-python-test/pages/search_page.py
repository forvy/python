from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from data.locators import SearchPageLocators
from selenium.webdriver.common.by import By


class SearchPage(BasePage):

    def __init__(self, driver, wait):
        self.url = "https://duckduckgo.com/"
        self.locator = SearchPageLocators
        super().__init__(driver, wait)

    def go_to_search_page(self):
        self.go_to_page(self.url)

    def check_title(self, title):
        self.wait.until(EC.title_contains(title))

    def make_a_search(self, input_text):
        self.driver.find_element(by=By.ID, value= 'searchbox_input').send_keys(input_text+u'\ue007')
        self.wait.until(EC.title_contains(input_text))
        self.driver.save_screenshot("results/results.png")
