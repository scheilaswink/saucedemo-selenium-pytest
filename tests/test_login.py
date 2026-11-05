import data
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestLogin:
    def test_login_with_valid_user(self, driver):
        login_page = LoginPage(driver)
        login_page.open(data.BASE_URL)
        login_page.login(data.STANDARD_USER, data.PASSWORD)
        assert InventoryPage(driver).get_title() == "Products"

    def test_login_with_locked_out_user(self, driver):
        login_page = LoginPage(driver)
        login_page.open(data.BASE_URL)
        login_page.login(data.LOCKED_OUT_USER, data.PASSWORD)
        assert "locked out" in login_page.get_error_message()

    def test_login_with_wrong_password(self, driver):
        login_page = LoginPage(driver)
        login_page.open(data.BASE_URL)
        login_page.login(data.STANDARD_USER, data.WRONG_PASSWORD)
        assert "do not match" in login_page.get_error_message()

    def test_login_with_empty_username(self, driver):
        login_page = LoginPage(driver)
        login_page.open(data.BASE_URL)
        login_page.login("", data.PASSWORD)
        assert "Username is required" in login_page.get_error_message()
