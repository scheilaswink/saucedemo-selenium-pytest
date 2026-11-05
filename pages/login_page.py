from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = BasePage.by_test_id("username")
    PASSWORD = BasePage.by_test_id("password")
    LOGIN_BUTTON = BasePage.by_test_id("login-button")
    ERROR_MESSAGE = BasePage.by_test_id("error")

    def open(self, url):
        self.driver.get(url)

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.text_of(self.ERROR_MESSAGE)
