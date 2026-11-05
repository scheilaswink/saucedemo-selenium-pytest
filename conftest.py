import pytest
from selenium import webdriver

import data
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # Evita o aviso de "senha vazada" do Chrome, que bloqueia a tela em testes automatizados
    options.add_experimental_option("prefs", {"profile.password_manager_leak_detection": False})
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def logged_in(driver):
    """Abre o site já logado com o usuário padrão e devolve a página de produtos."""
    login_page = LoginPage(driver)
    login_page.open(data.BASE_URL)
    login_page.login(data.STANDARD_USER, data.PASSWORD)
    return InventoryPage(driver)
