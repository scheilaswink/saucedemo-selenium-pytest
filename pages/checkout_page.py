from pages.base_page import BasePage


class CheckoutPage(BasePage):
    CHECKOUT_BUTTON = BasePage.by_test_id("checkout")
    FIRST_NAME = BasePage.by_test_id("firstName")
    LAST_NAME = BasePage.by_test_id("lastName")
    POSTAL_CODE = BasePage.by_test_id("postalCode")
    CONTINUE_BUTTON = BasePage.by_test_id("continue")
    FINISH_BUTTON = BasePage.by_test_id("finish")
    COMPLETE_HEADER = BasePage.by_test_id("complete-header")
    ERROR_MESSAGE = BasePage.by_test_id("error")

    def start_checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def fill_information(self, first_name, last_name, postal_code):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def finish(self):
        self.click(self.FINISH_BUTTON)

    def get_complete_message(self):
        return self.text_of(self.COMPLETE_HEADER)

    def get_error_message(self):
        return self.text_of(self.ERROR_MESSAGE)
