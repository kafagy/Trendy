import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# at the beginning:
start_time = time.time()

chromeOptions = Options()
chromeOptions.add_argument("--headless")
chromeOptions.add_experimental_option('prefs', {'geolocation': True})
driver = webdriver.Chrome(chrome_options=chromeOptions)
wait = WebDriverWait(driver, 30)
driver.get("https://facebook.com/")

# Typing credentials and signing in
wait.until(EC.visibility_of_element_located((By.ID, 'email')))
driver.find_element_by_id('email').send_keys('')
wait.until(EC.visibility_of_element_located((By.ID, 'pass')))
driver.find_element_by_id('pass').send_keys('')
wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="submit"]')))
driver.find_element_by_xpath('//input[@type="submit"]').click()

# Dialog box alert handler
try:
    notNowNotifcation = driver.find_element_by_xpath('//a[@action="cancel"]')
    if not notNowNotifcation is None:
        notNowNotifcation.click()
except:
    pass

# Clicks on the seemore buton
wait.until(EC.visibility_of_element_located((By.ID, 'u_ps_0_4_j')))
driver.find_element_by_id('u_ps_0_4_j').click()
time.sleep(3)

headlines = []
wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="_3-9y"]')))
spans = driver.find_elements_by_xpath('//span[@class="_3-9y"]')
for span in spans:
    trends = str(str(span.text).split('\n')[0:])
    headlines.append(trends)

print(headlines)

# Trends Links
links = []
wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[starts-with(@href, "/topic")]')))
hrefs = driver.find_elements_by_xpath('//a[starts-with(@href, "/topic")]')
for href in hrefs:
    links.append(href.get_attribute('href'))

for num in range(0, 10):
    print(headlines[num] + " : " + links[num])

# At the end of the program:
print("Retrieval time took %f seconds" % (time.time() - start_time))