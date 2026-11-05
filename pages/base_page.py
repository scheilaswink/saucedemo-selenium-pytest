from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Ações comuns a todas as páginas, com esperas explícitas."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @staticmethod
    def by_test_id(test_id):
        # O SauceDemo usa o atributo data-test em quase todos os elementos
        return (By.CSS_SELECTOR, f'[data-test="{test_id}"]')

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text

    def is_present(self, locator):
        return len(self.driver.find_elements(*locator)) > 0
