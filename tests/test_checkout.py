import data
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage


class TestCheckout:
    def test_complete_purchase(self, logged_in, driver):
        logged_in.add_to_cart(data.BACKPACK)
        logged_in.go_to_cart()
        checkout = CheckoutPage(driver)
        checkout.start_checkout()
        checkout.fill_information(data.FIRST_NAME, data.LAST_NAME, data.POSTAL_CODE)
        checkout.finish()
        assert checkout.get_complete_message() == "Thank you for your order!"

    def test_checkout_without_first_name(self, logged_in, driver):
        logged_in.add_to_cart(data.BACKPACK)
        logged_in.go_to_cart()
        checkout = CheckoutPage(driver)
        checkout.start_checkout()
        checkout.fill_information("", data.LAST_NAME, data.POSTAL_CODE)
        assert "First Name is required" in checkout.get_error_message()

    def test_checkout_without_postal_code(self, logged_in, driver):
        logged_in.add_to_cart(data.BACKPACK)
        logged_in.go_to_cart()
        checkout = CheckoutPage(driver)
        checkout.start_checkout()
        checkout.fill_information(data.FIRST_NAME, data.LAST_NAME, "")
        assert "Postal Code is required" in checkout.get_error_message()

    def test_logout_returns_to_login_page(self, logged_in, driver):
        logged_in.logout()
        # find() usa espera explícita até o botão de login aparecer
        assert LoginPage(driver).find(LoginPage.LOGIN_BUTTON).is_displayed()
