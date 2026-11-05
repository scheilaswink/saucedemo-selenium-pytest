"""Exploração: compara o comportamento dos usuários com problema com o standard_user."""
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.saucedemo.com/"
T = lambda d, t: d.find_element(By.CSS_SELECTOR, f'[data-test="{t}"]')

def new_driver():
    o = webdriver.ChromeOptions()
    o.add_argument("--headless=new"); o.add_argument("--window-size=1280,900")
    o.add_experimental_option("prefs", {"profile.password_manager_leak_detection": False})
    return webdriver.Chrome(options=o)

def login(d, user):
    d.get(URL); T(d,"username").send_keys(user); T(d,"password").send_keys("secret_sauce"); T(d,"login-button").click()
    WebDriverWait(d, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="inventory-list"]')))

def explore(user):
    d = new_driver(); r = {"user": user}
    try:
        login(d, user)
        r["images"] = sorted(set(i.get_attribute("src").split("/")[-1] for i in d.find_elements(By.CSS_SELECTOR, "img.inventory_item_img")))
        names = [e.text for e in d.find_elements(By.CSS_SELECTOR, '[data-test="inventory-item-name"]')]
        r["prices_before"] = [e.text for e in d.find_elements(By.CSS_SELECTOR, '[data-test="inventory-item-price"]')]
        Select(T(d,"product-sort-container")).select_by_value("lohi")
        r["prices_lohi"] = [e.text for e in d.find_elements(By.CSS_SELECTOR, '[data-test="inventory-item-price"]')]
        Select(T(d,"product-sort-container")).select_by_value("za")
        r["names_za_first"] = d.find_elements(By.CSS_SELECTOR, '[data-test="inventory-item-name"]')[0].text
        d.get(URL + "inventory.html")
        add_ok = {}
        for b in d.find_elements(By.CSS_SELECTOR, 'button[data-test^="add-to-cart-"]'):
            tid = b.get_attribute("data-test"); b.click()
            add_ok[tid.replace("add-to-cart-","")] = len(d.find_elements(By.CSS_SELECTOR, f'[data-test="{tid.replace("add-to-cart","remove")}"]')) > 0
        r["add_to_cart_works"] = add_ok
        badge = d.find_elements(By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]'); r["badge"] = badge[0].text if badge else "0"
        rem_ok = {}
        for b in d.find_elements(By.CSS_SELECTOR, 'button[data-test^="remove-"]'):
            tid = b.get_attribute("data-test"); b.click()
            rem_ok[tid.replace("remove-","")] = len(d.find_elements(By.CSS_SELECTOR, f'[data-test="{tid.replace("remove","add-to-cart")}"]')) > 0
        r["remove_works"] = rem_ok
        # checkout
        d.get(URL + "inventory.html")
        btns = d.find_elements(By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]')
        if btns: btns[0].click()
        T(d,"shopping-cart-link").click(); T(d,"checkout").click()
        T(d,"firstName").send_keys("Scheila"); T(d,"lastName").send_keys("Wink"); T(d,"postalCode").send_keys("13330")
        r["fields_after_typing"] = {k: T(d,k).get_attribute("value") for k in ("firstName","lastName","postalCode")}
        T(d,"continue").click()
        err = d.find_elements(By.CSS_SELECTOR, '[data-test="error"]'); r["checkout_error"] = err[0].text if err else None
        r["url_after_continue"] = d.current_url.split("/")[-1]
        if "step-two" in d.current_url:
            r["summary_total"] = T(d,"total-label").text
            T(d,"finish").click()
            r["url_after_finish"] = d.current_url.split("/")[-1]
            h = d.find_elements(By.CSS_SELECTOR, '[data-test="complete-header"]'); r["complete"] = h[0].text if h else None
    except Exception as e:
        r["exception"] = repr(e)[:300]
    finally:
        d.quit()
    return r

for u in ["standard_user", "problem_user", "error_user", "visual_user"]:
    print(json.dumps(explore(u), ensure_ascii=False))
