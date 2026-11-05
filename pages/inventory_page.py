from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = BasePage.by_test_id("title")
    CART_LINK = BasePage.by_test_id("shopping-cart-link")
    CART_BADGE = BasePage.by_test_id("shopping-cart-badge")
    SORT_SELECT = BasePage.by_test_id("product-sort-container")
    ITEM_PRICE = BasePage.by_test_id("inventory-item-price")
    MENU_BUTTON = ("id", "react-burger-menu-btn")
    LOGOUT_LINK = BasePage.by_test_id("logout-sidebar-link")

    def get_title(self):
        return self.text_of(self.TITLE)

    def add_to_cart(self, product):
        self.click(self.by_test_id(f"add-to-cart-{product}"))

    def remove_from_cart(self, product):
        self.click(self.by_test_id(f"remove-{product}"))

    def get_cart_count(self):
        if not self.is_present(self.CART_BADGE):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def sort_by(self, option_value):
        Select(self.find(self.SORT_SELECT)).select_by_value(option_value)

    def get_prices(self):
        return [float(p.text.replace("$", "")) for p in self.find_all(self.ITEM_PRICE)]

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
