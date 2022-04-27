from selenium import webdriver
import time

TIMEOUT = time.time() + 5
FIVE_MINUTES_TIMEOUT = time.time() + 5*60

chrome_driver_path = r"C:\Users\jackf\development\chromedriver.exe"
URL = "http://orteil.dashnet.org/experiments/cookie/"

driver = webdriver.Chrome(chrome_driver_path)
driver.get(URL)

#Get cookies to click
cookie = driver.find_element_by_id("cookie")

#Get the upgrade ids
upgrade_items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in upgrade_items]


while True:
    cookie.click()
    if time.time() >= TIMEOUT:
        current_cookie_count = driver.find_element_by_css_selector("#game #money").text
        if "," in current_cookie_count:
            current_cookie_count = current_cookie_count.replace(",", "")
        current_cookie_count = int(current_cookie_count)
        print(current_cookie_count)

        #Get pane to upgrade
        upgrade_counts = driver.find_elements_by_css_selector("#store b")
        price_pool = []
        for upgrade in upgrade_counts:
            price = upgrade.text
            if price:
                price = int(price.split("-")[1].strip().replace(",",""))
                price_pool.append(price)

        #put all upgrade id <--> count into a new dictionary
        cookie_upgrades = {}
        for i in range(len(price_pool)):
            cookie_upgrades[price_pool[i]] = item_ids[i]

        #find upgrade we can afford now
        affordable_pool = {}
        for cost,id in cookie_upgrades.items():
            if current_cookie_count >= cost:
                affordable_pool[cost] = id

        #get the maximun level of upgrades
        highest_upgrade_cost = max(affordable_pool)
        print(highest_upgrade_cost)
        highest_upgrade_id = affordable_pool[highest_upgrade_cost]

        driver.find_element_by_id(highest_upgrade_id).click()

        TIMEOUT = time.time() + 5

    #Stop the program after 5 mins
    if time.time() > FIVE_MINUTES_TIMEOUT:
        apm = driver.find_element_by_id("cps").text
        print(apm)
        break
