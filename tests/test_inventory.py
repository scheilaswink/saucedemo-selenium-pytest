import data


class TestInventory:
    def test_add_one_item_updates_cart_badge(self, logged_in):
        logged_in.add_to_cart(data.BACKPACK)
        assert logged_in.get_cart_count() == 1

    def test_add_two_items_updates_cart_badge(self, logged_in):
        logged_in.add_to_cart(data.BACKPACK)
        logged_in.add_to_cart(data.BIKE_LIGHT)
        assert logged_in.get_cart_count() == 2

    def test_remove_item_clears_cart_badge(self, logged_in):
        logged_in.add_to_cart(data.BACKPACK)
        logged_in.remove_from_cart(data.BACKPACK)
        assert logged_in.get_cart_count() == 0

    def test_sort_by_price_low_to_high(self, logged_in):
        logged_in.sort_by("lohi")
        prices = logged_in.get_prices()
        assert prices == sorted(prices)

    def test_sort_by_price_high_to_low(self, logged_in):
        logged_in.sort_by("hilo")
        prices = logged_in.get_prices()
        assert prices == sorted(prices, reverse=True)
