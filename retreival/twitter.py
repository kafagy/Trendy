import time, pymysql.cursors, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# at the beginning:
start_time = time.time()
connection = pymysql.connect(user='root', password='abc123', host='127.0.0.1', db='trendy', cursorclass=pymysql.cursors.DictCursor, use_unicode=True, charset="utf8mb4")

chromeOptions = Options()
chromeOptions.add_argument("--headless")
chromeOptions.add_experimental_option('prefs', {'geolocation': True})
driver = webdriver.Chrome(chrome_options=chromeOptions)
wait = WebDriverWait(driver, 30)
driver.get("https://twitter.com/")

# Click on login button
wait.until(EC.visibility_of_element_located((By.XPATH, '//a[text()="Log in"]')))
driver.find_element_by_xpath('//a[text()="Log in"]').click()

# Typing credentials and signing in
wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="text-input email-input js-signin-email"]')))
driver.find_element_by_xpath('//input[@class="text-input email-input js-signin-email"]').send_keys('')
wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="password"]')))
driver.find_element_by_xpath('//input[@type="password"]').send_keys('')
wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="submit"]')))
driver.find_element_by_xpath('//input[@type="submit"]').click()

# Trends text
trends = []
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.u-linkComplex-target.trend-name')))
divs = driver.find_elements_by_css_selector('.u-linkComplex-target.trend-name')
for div in divs:
    if str(div.text)[0] == '#':
        trends.append(div.text)
    else:
        trends.append("#" + div.text)

# Trends links
links = []
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.pretty-link.js-nav.js-tooltip.u-linkComplex')))
hrefs = driver.find_elements_by_css_selector('.pretty-link.js-nav.js-tooltip.u-linkComplex')
for href in hrefs:
    links.append(href.get_attribute('href'))

for i in range(0, len(links)):
    print(trends[i] + " : " + links[i])

username = sys.argv[1]
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM trendy.twitter WHERE username = %s", username)
    if cursor.rowcount == 0:
        for i in range(0, len(links)):
            print(trends[i] + " : " + links[i])
            sql = "INSERT INTO trendy.twitter(id, username, trend, link, loadtime) VALUES (DEFAULT, %s, %s, %s, NOW())"
            cursor.execute(sql, (username, trends[i], links[i]))
        connection.commit()
    elif cursor.rowcount == 10:
        cursor.execute("DELETE FROM trendy.twitter WHERE username = %s", username)
        for i in range(0, len(links)):
            print(trends[i] + " : " + links[i])
            sql = "INSERT INTO trendy.twitter(id, username, trend, link, loadtime) VALUES (DEFAULT, %s, %s, %s, NOW())"
            cursor.execute(sql, (username, trends[i], links[i]))
        connection.commit()


# At the end of the program:
connection.close()
driver.quit()
print("Retrieval time took %f seconds" % (time.time() - start_time))
