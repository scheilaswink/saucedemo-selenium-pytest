import json, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException

URL = "https://www.saucedemo.com/"
T = lambda d, t: d.find_element(By.CSS_SELECTOR, f'[data-test="{t}"]')
def drv():
    o = webdriver.ChromeOptions(); o.add_argument("--headless=new"); o.add_argument("--window-size=1280,900")
    o.add_experimental_option("prefs", {"profile.password_manager_leak_detection": False})
    return webdriver.Chrome(options=o)
def login(d,u):
    d.get(URL); T(d,"username").send_keys(u); T(d,"password").send_keys("secret_sauce"); T(d,"login-button").click()
    WebDriverWait(d,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'[data-test="inventory-list"]')))
def alert_text(d):
    try:
        a=d.switch_to.alert; t=a.text; a.accept(); return t
    except NoAlertPresentException: return None

for u in ["standard_user","problem_user","error_user"]:
    d=drv(); r={"user":u}
    try:
        login(d,u)
        if u=="error_user":
            Select(T(d,"product-sort-container")).select_by_value("za"); r["sort_alert"]=alert_text(d)
            add={}
            for b in d.find_elements(By.CSS_SELECTOR,'button[data-test^="add-to-cart-"]'):
                tid=b.get_attribute("data-test"); b.click(); al=alert_text(d)
                add[tid[12:]]=(len(d.find_elements(By.CSS_SELECTOR,f'[data-test="{tid.replace("add-to-cart","remove")}"]'))>0, al)
            r["add"]=add
            rem={}
            for b in d.find_elements(By.CSS_SELECTOR,'button[data-test^="remove-"]'):
                tid=b.get_attribute("data-test"); b.click(); al=alert_text(d)
                rem[tid[7:]]=(len(d.find_elements(By.CSS_SELECTOR,f'[data-test="{tid.replace("remove","add-to-cart")}"]'))>0, al)
            r["remove"]=rem
            d.get(URL+"inventory.html")
        else:
            T(d,"add-to-cart-sauce-labs-backpack").click()
        T(d,"shopping-cart-link").click(); T(d,"checkout").click()
        T(d,"firstName").send_keys("Scheila"); r["after_first"]={k:T(d,k).get_attribute("value") for k in ("firstName","lastName")}
        T(d,"lastName").send_keys("Wink"); r["after_last"]={k:T(d,k).get_attribute("value") for k in ("firstName","lastName")}
        T(d,"postalCode").send_keys("13330")
        T(d,"continue").click(); time.sleep(1)
        err=d.find_elements(By.CSS_SELECTOR,'[data-test="error"]'); r["error"]=err[0].text if err else None
        r["url"]=d.current_url.split("/")[-1]
        if "step-two" in d.current_url:
            T(d,"finish").click(); time.sleep(1); r["alert_finish"]=alert_text(d)
            r["url_finish"]=d.current_url.split("/")[-1]
    except Exception as e: r["exc"]=repr(e)[:200]
    finally: d.quit()
    print(json.dumps(r,ensure_ascii=False))
